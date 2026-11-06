# GM Powertrain Reference (E38 ECM, T43 TCM, FPCM)

Living reference for Tuner Tool Pro. Read this first when working on GM PIDs, scaling or diagnostics, and add to it as
things are learned. Start a new entry in the changelog at the bottom with every edit.

**How to read the confidence tags.** Every fact carries one:

| Tag | Meaning |
|---|---|
| **VERIFIED-CAR** | Read off the owner's car and checked (the app marks these `verified`). |
| **STANDARD** | Written in a public standard (SAE J1979 / ISO 15765-4). |
| **REPORT** | Stated in the owner's engineering report PDF; nobody has checked it on the car. |
| **APP-DATA** | Held in the app's PID data (Torque Pro list, T43 list). Origin is third-party; not proven on the car. |
| **UNVERIFIED** | A claim that looks wrong, unlikely or untestable from here. Do not rely on it. |

Sources used so far: the owner's two PDFs ("2.7Bar MAP Sensor PID Tuning", "Comprehensive Engineering Report: GM E38 ECM,
T43 TCM, and FPCM Communications…"), the Torque Pro extraction in `torque-pro-main/5-extracted-data/` (see
`docs/torque-extraction-import.md`), and the PID data in `app/tunertoolpro/data/` and `scanner/pid_table.py`.
Primary-source findings from the background research pass go in `docs/research/gm-primary-sources.md` when it lands;
nothing from it is in this file yet.

---

## 1. The car and the network

Target vehicle (REPORT): VE Series II Commodore, L77 6.0 L V8, E38 ECM, 6L80E six-speed with the internal T43 TCM,
returnless fuel system with an FPCM, forced induction on E85, Proflow PFEFI-MAP2 2.7 bar MAP sensor, Circle D 3200 stall
converter, 1500 cc injectors, KPM dual-pump module.

| Node | Request ID | Response ID | Confidence |
|---|---|---|---|
| E38 ECM | 7E0 | 7E8 | STANDARD (J1979 / GM convention) |
| T43 TCM (inside the TEHCM) | 7E2 | 7EA | APP-DATA, REPORT; `22199A` on 7E2 is VERIFIED-CAR |
| FPCM | 7E3 | 7EB | REPORT only. **Not confirmed**: no PID in the app has been read from 7E3 |
| Functional broadcast | 7DF | 7E8… | STANDARD |

- Bus: GMLAN high-speed CAN, 500 kbit/s, 11-bit identifiers, ISO 15765-4 (STANDARD).
- Mode 01 requests sent to 7E0 or broadcast reach the ECM; they bypass the TCM. TCM data needs Mode 22 to 7E2 (REPORT, matches the app).
- GM Mode 22 DIDs are two bytes (`22 HH LL`). Their meaning is module-specific and not public; every equation below that is
  not VERIFIED-CAR came from a scraped list or an AI-written report.

## 2. MAP sensor and PID 010B

### What the report says (REPORT)
- Sensor: Proflow PFEFI-MAP2, 0.5 V to 4.5 V output.
- Transfer: `MAP_kPa = V × 62.5 − 11.25` (linear 312.5, offset −11.25). Worked values: 0.5 V → 20.0 kPa, 4.5 V → 270.0 kPa, 5 V → 301.25 kPa.
- For a one-byte PID 0B read as 0 V…5 V: `MAP = (A / 255) × 312.5 − 11.25`. Byte examples: `0x1A` → 20.6 kPa, `0xE5` → 269.4 kPa, `0xFF` → 301.25 kPa.
- Boost (psi): `(MAP_kPa − BARO_kPa) × 0.145038`, with BARO from PID 0133 or 101.325 kPa.
- Claims the factory E38 OS caps PID 010B at 151.3 kPa and needs a custom OS (HP Tuners 2/3-bar or EFILive) to log beyond it.

### What the app does now (core v0.4.1)
`scanner/pid_table.py` 010B: `max(0, A/255 × 312.5 − 11.25)`, shown 0–300 kPa. It replaces the old 3 bar scaling (`A/255 × 300`).
The clamp matches the report's own Java sample. The sensor is owner-confirmed (fork session). The scaling is **not** checked against a gauge.

### The risk, and the test that settles it (read before trusting boost numbers)
SAE J1979 defines PID 0B as **one byte = kPa directly** (0–255 kPa) (STANDARD). On a stock OS the right decode is `A`, not the
voltage-style formula above. The report's formula only holds if the custom OS deliberately rescales PID 0B so the byte spans
0–5 V. Nobody has shown that. A wrong guess here is a roughly 20 % error in the displayed boost, which on a tune is a safety issue.

Key-on engine-off check (atmospheric pressure, about 101 kPa at sea level):

| Raw byte shown | Meaning |
|---|---|
| about `0x65` (101) | PID 0B is plain kPa. The 2.7 bar formula is **wrong** for this OS; use `A`. |
| about `0x5C` (92) | PID 0B is the report's rescaled form. The new scaling is right. |

Then compare the decoded value with PID 0133 (baro) and a mechanical gauge under boost. Until done, treat boost from 010B as unconfirmed.
Also unproven: the 151.3 kPa cap (the figure is not a clean one-byte limit) and whether the E38 ever stops advancing the VVE table there. UNVERIFIED.

## 3. T43 / 6L80E transmission

- Ratios (STANDARD for the 6L80): 1st 4.027, 2nd 2.364, 3rd 1.532, 4th 1.152, 5th 0.852, 6th 0.667, reverse about 3.06.
  The app uses these to imply the gear from turbine/output speed (`live.py`).
- Verified in code: `22199A` current gear (7E2, VERIFIED-CAR); `221941` input shaft speed and `221942` output shaft speed,
  both `((A*256)+B)/4` or `×0.125` (two formulas in the list; see `scanner/t43_pids.py` for how the app picks).
- Driveability notes (REPORT, tuning folklore not tested here):
  - Stall on deceleration with a high-stall converter: keep TCC desired-slip tables active in low gears and disable low-speed lockup.
  - Power drop on 2-3 upshift under boost: ECM upshift torque management retards timing, up to about a second. Report suggests
    a factor of 0.5–0.7 and more line pressure. A tune change; confirm in the calibration tool, not here.

## 4. FPCM and the fuel system

- FPCM takes a target pressure from the ECM over CAN and drives the pump by PWM. Sensor is in-line. Header 7E3 (REPORT, not confirmed).
- Report's scenario: at 9 psi boost on E85, rail pressure falls 58 psi → 40 psi against a 50.7 psi minimum. Causes given: voltage drop in
  14 AWG wire at 35–45 A, E85's higher volume demand, and the returnless PWM reaching 100 %.
- Treat the numbers as **UNVERIFIED**: the ">3 V drop" and "14.2 V → under 11 V" figures are not derived from a wire length; the
  conductor resistance is never stated. The mechanism (undersized harness, duty pinned at 100 %) is plausible and cheap to check:
  log pump duty and supply voltage together under load.
- What the app can log for it, all unconfirmed on the car:
  - `221471` FPCM duty cycle (7E3), `A × 0.392157` %: in the `gm-report-extras` pack.
  - `0123` fuel rail pressure (kPa ×10), `0122` rail pressure relative to manifold (×0.079), `010A` low-side pressure (×3), `0142` module voltage, `221141` ignition feed voltage: in the Generic OBD-II packs or the catalogue.

## 5. PID conflict register (important)

The report reuses PIDs the app already holds, with different meanings. The app's data was **not** changed to match the report.

| PID | App has | Report says | Decision |
|---|---|---|---|
| `221198` | Injector pulse width cyl 6 (Torque GM list), `(A<<8+B)/65.535` ms | Target fuel rail pressure, ×0.0145 psi | Keep app. Report claim unproven. |
| `221199` | Injector pulse width cyl 7 on the ECM | FPCM measured fuel pressure, header 7E3, ×0.0145 psi | Keep app. A 7E3 read may be different, but a PID table keyed by ID alone would collide. Not added. |
| `221993` | "1-2 shift time" `A/40` (ambiguous in the app) | Signed TCC slip `((A*256+B)−32768)/4` | Keep app, flagged ambiguous. Not added. |
| `221935`, `221934` | not present; app uses `221941`/`221942` for speeds | Input/output shaft speed `/4` | Not added; probable duplicates of the verified pair under wrong IDs. |
| `22199B` | not present; `22199A` is VERIFIED-CAR current gear | Current engaged gear | Not added; probable typo for `22199A`. |
| `22153E` | oil temp is `221154` | Oil temp `A−40` | Added as a second candidate in `gm-report-extras`. |

**Kotlin defect (VE_CALAIS_Scanner, not mine to edit):** `pidMap = standardPidMap + cylinderPidMap`, the right side wins on duplicate
keys. The fork's new `221199` FPCM entry is therefore dead code (the cylinder map's injector entry overrides it), so the app would
decode FPCM pressure as injector pulse width. The cylinder map's `221198` carries a note that it may be fuel rail pressure.

## 6. Where each fact lives in the app

| Thing | Location |
|---|---|
| Core PID catalogue, 010B | `scanner/pid_table.py` (core repo; vendored into `app/` and `android/`) |
| T43 PIDs and gear logic | `scanner/t43_pids.py`, `live.py` |
| Torque-format packs | `data/*.csv`, listed in `scanner/predefined.py` |
| Safe CSV reader | `scanner/torque_csv.py` (Mode 01/22 only; Mode 21 only with the module opt-in; equations limited to A–D and a few operators) |
| Packs added this session | `ford` (44), `generic-obd2-more` (14), `gm-report-extras` (6, unconfirmed) |
| What the Torque extraction contributed or was rejected | `docs/torque-extraction-import.md` |

Never edit the vendored copies in `app/tunertoolpro` or `android/tunertoolpro`; change the core repo, tag, and run `tools/update_core.py <tag>`.

## 7. Verify-on-car checklist

1. Key-on engine-off: raw `010B` byte vs baro (section 2). Decide the real PID 0B scaling.
2. Compare boost from `010B` with a mechanical gauge at 3 or 4 points.
3. Request `221471` from header 7E3; if there is no response, the FPCM is not at 7E3 and the section 4 assumption is wrong.
4. Request `222006`, `22153E`, `221938`, `221939`, `22193E` and compare to known temperatures and states.
5. Decide `221198`/`221199`/`221993` by reading them at idle and at load and seeing which meaning moves.
6. Log pump duty and supply voltage together on a pull, to check the fuel-pressure collapse story.

## 8. Open questions

- Is the FPCM really a separate diagnostic node at 7E3, or does that data come through another module?
- Does the owner's custom OS rescale PID 0B, and is it HP Tuners or EFILive?
- Which of the T43's Mode 22 DIDs answer on this car beyond the verified ones?

## Changelog

- 2026-11-07: file created. Added 2.7 bar MAP decode (core v0.4.1), `gm-report-extras` pack, the conflict register and the PID 0B scaling test.
  Primary-source research agent still running; its file is not merged.
