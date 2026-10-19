# 2002 VY SS Commodore Wrecking – Parts List

A single-page parts list for the wrecked VY SS. Buyers claim parts, you confirm sales from Seller View. Data is stored in a Firebase Realtime Database.

## Files

- `index.html` – the whole app (Tailwind, Font Awesome and Firebase load from CDNs).
- `database.rules.json` – the security rules for the database (see step 2 below).
- `firebase.json`, `.firebaserc` – only needed if you deploy the rules with the Firebase CLI.
- `20261018_091055.jpg` – hero photo. **Add it to this folder** (the page shows a broken image until you do).

## 1. One-time Firebase setup

The page shows an error banner (and no parts) until the database exists and the rules are published.

1. Go to <https://console.firebase.google.com> and open your project (`vyss-wrecking`).
2. Build → **Realtime Database** → **Create Database**. Pick a location and start in **locked mode**.
   - Realtime Database only offers `us-central1` (Iowa), `europe-west1` (Belgium) and `asia-southeast1` (Singapore). Singapore is the closest to Australia. See <https://firebase.google.com/docs/database/locations>.
3. Copy the database URL shown at the top of the **Data** tab.
   - `us-central1` URLs look like `https://NAME.firebaseio.com`.
   - Other regions look like `https://NAME.asia-southeast1.firebasedatabase.app`.
   - If it differs from the `databaseURL` near the top of the script in `index.html`, replace that value with yours.

## 2. Publish the security rules

Either paste the contents of `database.rules.json` into the **Rules** tab and click **Publish**, or deploy with the CLI from this folder:

```bash
npx firebase-tools login
npx firebase-tools deploy --only database --project <your-project-id>
```

What the rules allow:

- Anyone can read the parts list.
- Anyone can change a part's `status` (`available` / `pending` / `sold`). The buyer claim and the seller buttons both need this.
- Nobody can change a part's name, price or removal fee, delete a part, add extra fields, or write anywhere else. Edit prices in the Firebase console (the console bypasses the rules).

What they cannot do: stop a stranger who has the database URL from flipping a part's status. The seller PIN in `index.html` (`SECRET_PIN`) is visible in the page source and only hides the admin buttons. Real seller-only protection needs Firebase Authentication. Rules reference: <https://firebase.google.com/docs/database/security>.

## 3. Host it on your own device

Option A – open it directly: double-click `index.html`. Needs internet for the CDNs and Firebase.

Option B – serve it on your home network (phone/tablet on the same Wi-Fi):

```bash
cd vy-wrecking
python3 -m http.server 8000
```

Find your computer's address with `hostname -I` (Linux), `ipconfig getifaddr en0` (Mac) or `ipconfig` (Windows), then open `http://<address>:8000` on the other device. The terminal must stay open while the page is being used.

## Take it down when the car is sold

- Stop the server with `Ctrl+C`, or delete the folder.
- Delete the database (or its `parts` node) in the Firebase console so nothing is left online.

Buyers outside your Wi-Fi can't reach a page served from your computer. For them you would need a public host (for example GitHub Pages or Netlify).
