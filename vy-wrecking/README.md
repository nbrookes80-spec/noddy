# 2002 VY SS Commodore Wrecking – Parts List

A single-page parts list for the wrecked VY SS. Buyers claim parts and leave their name and phone number; you confirm sales from Seller View. Data is stored in a Firebase Realtime Database and the page is hosted on Firebase Hosting.

**Live link to send buyers:** <https://vy-ss-wrecking.web.app>

## Files

- `index.html` – the whole app (Tailwind, Font Awesome and Firebase load from CDNs).
- `site-config.js` – public values the page needs: the seller's public encryption key and a salt. Safe to publish.
- `database.rules.json` – the database security rules.
- `tools/` – `set-pin.js` (set or change the seller PIN) and `decrypt-claims.js` (read buyer details).
- `keybundle.json` – **private, not committed, not published.** Your encryption private key, locked with the PIN. Back it up somewhere private.
- `firebase.json`, `.firebaserc` – Firebase CLI config (project `vy-ss-wrecking`). Hosting publishes only the page, `site-config.js` and the photo.
- `NEW-PIN.txt` – **private, not committed, not published.** Written by `set-pin.js`; holds the current seller PIN.
- `photos/01.jpg` … `11.jpg` – web-sized copies (1800px, metadata stripped) shown in the carousel. The original camera files (`2026*.jpg`) are ignored by git and not hosted.

## How the protection works

- **Buyer details are encrypted in the buyer's browser** (AES-GCM, with the key sealed by your RSA public key) before being sent. The database only ever holds ciphertext, and nobody can read the `claims` node from the page.
- **Seller actions need the PIN.** Marking sold, resetting or cancelling a claim carries a PIN-derived proof (PBKDF2, 600k rounds) that the database rules check on the server. The PIN is not in the page source. Buyers can only move a part from `available` to `pending`.
- **Parts are locked down.** Nobody can create or delete parts or change a name, price or removal fee from the page. Edit those in the Firebase console.
- Page output is HTML-escaped, and the host sends anti-framing, no-sniff, no-referrer and HSTS headers.

### Reading buyer details

```bash
node tools/decrypt-claims.js
```

It prompts for the PIN, fetches `claims` with the Firebase CLI and decrypts locally. The Seller View bell still shows which parts are pending.

### Rotating the PIN

```bash
OLD_PIN=<current> node tools/set-pin.js
```

This generates a new random PIN (16 characters from an unambiguous alphabet, ~80 bits), re-locks `keybundle.json`, updates the verifier in the database and writes the new PIN to `NEW-PIN.txt` (overwriting the old one). The terminal shows only the file path. Nothing needs redeploying. Save the PIN in a password manager, then delete `NEW-PIN.txt`. To pick your own instead, add `PIN=<new>`.

### Photos

The carousel reads the `PHOTOS` list near the end of the script in `index.html`. To change photos, resize new ones into `photos/`, update that list and redeploy hosting. Arrows, swipe, the dots, and the left/right keys move between photos; the expand button (or clicking the front photo) opens a full-screen viewer, closed with Esc or the × button.

## Deploying

Re-run from this folder after any change (`npx firebase-tools login` once):

```bash
npx firebase-tools deploy --only database   # security rules
npx firebase-tools deploy --only hosting    # the page
```

Do not paste the rules into the console Rules editor by hand; its auto-closing brackets corrupt them.

## Loading or resetting the parts list

Clients can't create parts, so an admin loads them: Firebase console → Realtime Database → Data → `parts` → ⋮ → **Import JSON**, an object keyed by part id whose `id` field equals the key:

```json
{ "ls1_engine": { "id": "ls1_engine", "name": "LS1 5.7L V8 Engine (Running)", "price": 2800, "removalFee": 300, "status": "available" } }
```

The original 14 parts are in `seedParts` in `index.html`. Edit prices and names in the console.

## Testing locally

```bash
python3 -m http.server 8000
```

then browse to `http://localhost:8000` (encryption needs https or localhost). It uses the live database, so a test claim changes real data: reset the part in Seller View and clear test entries under `claims` in the console.

## Limits to know about

- **The PIN is the lock.** Two things depend on it: the online check on seller actions, and the lock on `keybundle.json`. The generated PIN is long enough that guessing is not practical. A short PIN you choose yourself is not, so avoid `PIN=` with something short. Keep `keybundle.json` and `NEW-PIN.txt` private.
- Phone-width layout of the carousel has not been verified on a real phone.
- If you lose `keybundle.json`, existing buyer details cannot be decrypted. Buyers' details are readable only to someone holding that file and the PIN.
- Anyone can still claim parts (move them to `pending`), so a prankster can tie up the list. You clear it from Seller View.
- The database URL is public, so enable Firebase App Check or delete the database when the car is sold.
- Real seller-only access would use Firebase Authentication instead of a PIN.

## Take it down when the car is sold

```bash
npx firebase-tools hosting:disable
```

Then delete the database (or its `parts` and `claims` nodes) in the Firebase console so no buyer details are left online.
