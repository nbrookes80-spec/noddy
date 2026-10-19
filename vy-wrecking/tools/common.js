const crypto = require("crypto");

const ITERATIONS = 600000;
const INSTANCE = "vy-ss-wrecking-default-rtdb";

const derive = (pin, saltB64) => crypto.pbkdf2Sync(pin, Buffer.from(saltB64, "base64"), ITERATIONS, 32, "sha256");

function wrap(privateDer, pin, keySalt) {
  const iv = crypto.randomBytes(12);
  const cipher = crypto.createCipheriv("aes-256-gcm", derive(pin, keySalt), iv);
  const body = Buffer.concat([cipher.update(privateDer), cipher.final(), cipher.getAuthTag()]);
  return { keySalt, iv: iv.toString("base64"), wrappedPrivateKey: body.toString("base64") };
}

function unwrap(bundle, pin) {
  const body = Buffer.from(bundle.wrappedPrivateKey, "base64");
  const decipher = crypto.createDecipheriv("aes-256-gcm", derive(pin, bundle.keySalt), Buffer.from(bundle.iv, "base64"));
  decipher.setAuthTag(body.subarray(body.length - 16));
  try {
    return Buffer.concat([decipher.update(body.subarray(0, body.length - 16)), decipher.final()]);
  } catch {
    throw new Error("Wrong PIN, or keybundle.json is damaged.");
  }
}

module.exports = { crypto, ITERATIONS, INSTANCE, derive, wrap, unwrap };
