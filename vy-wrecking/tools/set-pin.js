// Sets or changes the seller PIN.
//   First run:  PIN=xxxx node tools/set-pin.js
//   Change PIN: OLD_PIN=xxxx PIN=yyyy node tools/set-pin.js
const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");
const { crypto, INSTANCE, derive, wrap, unwrap } = require("./common");

const root = path.join(__dirname, "..");
const bundlePath = path.join(root, "keybundle.json");
const sitePath = path.join(root, "site-config.js");
const pin = process.env.PIN;
if (!pin) {
  console.error("Set PIN (and OLD_PIN when changing it).");
  process.exit(1);
}

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
console.log("PIN set. Back up keybundle.json somewhere private; without it buyer details cannot be decrypted.");
