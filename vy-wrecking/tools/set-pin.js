// Sets or rotates the seller PIN. Without PIN set, a strong random one is generated
// and written to NEW-PIN.txt (never committed or published).
//   First run:  node tools/set-pin.js
//   Rotate:     OLD_PIN=<current> node tools/set-pin.js
//   Choose own: OLD_PIN=<current> PIN=<new> node tools/set-pin.js
const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");
const { crypto, INSTANCE, derive, wrap, unwrap } = require("./common");

const root = path.join(__dirname, "..");
const bundlePath = path.join(root, "keybundle.json");
const sitePath = path.join(root, "site-config.js");
const ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
const generated = !process.env.PIN;
const pin = process.env.PIN || Array.from({ length: 4 }, () =>
  Array.from({ length: 4 }, () => ALPHABET[crypto.randomInt(ALPHABET.length)]).join("")).join("-");

let privateDer, keySalt, adminSalt, publicKey;
if (fs.existsSync(bundlePath) && fs.existsSync(sitePath)) {
  if (!process.env.OLD_PIN) {
    console.error("Keys already exist. Set OLD_PIN to change the PIN.");
    process.exit(1);
  }
  const bundle = JSON.parse(fs.readFileSync(bundlePath, "utf8"));
  privateDer = unwrap(bundle, process.env.OLD_PIN);
  keySalt = bundle.keySalt;
  const site = JSON.parse(fs.readFileSync(sitePath, "utf8").replace(/^[^{]*/, "").replace(/;\s*$/, ""));
  adminSalt = site.adminSalt;
} else {
  const pair = crypto.generateKeyPairSync("rsa", { modulusLength: 2048 });
  privateDer = pair.privateKey.export({ format: "der", type: "pkcs8" });
  publicKey = pair.publicKey.export({ format: "jwk" });
  keySalt = crypto.randomBytes(16).toString("base64");
  adminSalt = crypto.randomBytes(16).toString("base64");
  fs.writeFileSync(sitePath, "window.SITE_CONFIG = " + JSON.stringify({ publicKey, adminSalt }, null, 2) + ";\n");
}

fs.writeFileSync(bundlePath, JSON.stringify(wrap(privateDer, pin, keySalt), null, 2) + "\n", { mode: 0o600 });

const verifier = derive(pin, adminSalt).toString("base64");
execFileSync("npx", ["--yes", "firebase-tools", "database:set", "/config/adminVerifier", "--force", "--instance", INSTANCE],
  { cwd: root, input: JSON.stringify(verifier), stdio: ["pipe", "inherit", "inherit"] });
const note = path.join(root, "NEW-PIN.txt");
fs.writeFileSync(note, [
  "VY Wrecking seller PIN",
  "Set: " + new Date().toLocaleString(),
  "",
  "PIN: " + pin,
  "",
  "Enter it in Seller View on the page, and when running: node tools/decrypt-claims.js",
  "Save it in a password manager, then delete this file. It is not committed or published.",
  "Back up keybundle.json too; without it buyer details cannot be decrypted.",
  ""
].join("\n"), { mode: 0o600 });
fs.chmodSync(note, 0o600);
console.log(`PIN ${generated ? "generated and " : ""}set. It is saved in ${note}`);
