// Fetches buyer claims from the database and decrypts them locally.
//   node tools/decrypt-claims.js          (prompts for the PIN; PIN env var also works)
const fs = require("fs");
const path = require("path");
const readline = require("readline");
const { execFileSync } = require("child_process");
const { crypto, INSTANCE, unwrap } = require("./common");

const root = path.join(__dirname, "..");

function askPin() {
  if (process.env.PIN) return Promise.resolve(process.env.PIN);
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout, terminal: true });
  rl._writeToOutput = (s) => { if (s.includes("PIN:")) process.stdout.write(s); };
  return new Promise((resolve) => rl.question("Seller PIN: ", (a) => { rl.close(); process.stdout.write("\n"); resolve(a); }));
}

(async () => {
  const bundle = JSON.parse(fs.readFileSync(path.join(root, "keybundle.json"), "utf8"));
  const key = crypto.createPrivateKey({ key: unwrap(bundle, await askPin()), format: "der", type: "pkcs8" });

  let claims = {};
  try {
    const raw = execFileSync("npx", ["--yes", "firebase-tools", "database:get", "/claims", "--instance", INSTANCE], { cwd: root, encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] });
    claims = raw.includes("{") ? JSON.parse(raw.slice(raw.indexOf("{"))) : {};
  } catch {
    console.log("No claims found (the node is empty, or the CLI could not reach the database: try `npx firebase-tools login`).");
    return;
  }
  const rows = Object.values(claims).sort((a, b) => a.createdAt - b.createdAt).map((c) => {
    try {
      const aes = crypto.privateDecrypt({ key, padding: crypto.constants.RSA_PKCS1_OAEP_PADDING, oaepHash: "sha256" }, Buffer.from(c.k, "base64"));
      const body = Buffer.from(c.ct, "base64");
      const d = crypto.createDecipheriv("aes-256-gcm", aes, Buffer.from(c.iv, "base64"));
      d.setAuthTag(body.subarray(body.length - 16));
      const who = JSON.parse(Buffer.concat([d.update(body.subarray(0, body.length - 16)), d.final()]).toString("utf8"));
      return { time: new Date(c.createdAt).toLocaleString(), part: c.partName, name: who.name, phone: who.phone };
    } catch {
      return { time: new Date(c.createdAt).toLocaleString(), part: c.partName, name: "(could not decrypt)", phone: "" };
    }
  });
  rows.length ? console.table(rows) : console.log("No claims yet.");
})().catch((e) => { console.error(e.message); process.exit(1); });
