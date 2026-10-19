# 2002 VY SS Commodore Wrecking – Parts List

A single-page parts list for the wrecked VY SS. Buyers claim parts, you confirm sales from Seller View. Data is stored in Firebase Realtime Database (`vyss-wrecking-default-rtdb`).

## Files

- `index.html` – the whole app (Tailwind, Font Awesome and Firebase load from CDNs).
- `20261018_091055.jpg` – hero photo. **Not in the repo yet – add it to this folder** (the page shows a broken image until you do).

## Host it on your own device

Option A – open it directly: double-click `index.html`. Needs internet for the CDNs and Firebase.

Option B – serve it on your home network (phone/tablet on the same Wi-Fi):

```bash
cd vy-wrecking
python3 -m http.server 8000
```

Then open `http://<your-computer-IP>:8000` on the other device. Find the IP with `ipconfig` (Windows) or `ifconfig` / `ip addr` (Mac/Linux).

## Take it down when the car is sold

- Stop the server with `Ctrl+C`, or delete the folder.
- Delete the `parts` data in the Firebase console (Realtime Database → delete the `parts` node) so nothing is left online.

## Before sharing the link more widely

- **The seller PIN is visible in the page source** (`SECRET_PIN` in `index.html`). It only hides the admin buttons from casual visitors.
- **Lock down the Firebase rules.** With open rules, anyone who finds the database URL can change part statuses. Set rules so the public can read but not write, and use Firebase Authentication if buyers need to claim parts.
- Buyers can only reach the page if it is hosted somewhere they can open. Hosting on your own device works only while it is running and only on your network. For buyers outside your network you would need a public host (for example GitHub Pages or Netlify).
