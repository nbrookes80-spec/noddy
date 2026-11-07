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

Primary-source research (GMW3110 via a third-party mirror, SAE/ISO text where obtainable, regulations) is in
`docs/research/gm-primary-sources.md`. Its findings are merged below and are marked where they correct earlier claims.

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
| T43 TCM (inside the TEHCM) | 7E2 | 7EA | Slot is GMW3110 'OBD ECU #3', which names no module. 'TCM on 7E2' is conventional, UNVERIFIED for this VE. `22199A` on 7E2 is VERIFIED-CAR, so the node answers |
| FPCM | 7E3 | 7EB | Slot is GMW3110 'OBD ECU #4' with no function. **No primary support for an FPCM on 7E3.** Discover on the car from the ECM's supported-ID responses |
| Functional broadcast | 7DF | 7E8… | STANDARD |

- Bus: GMLAN high-speed CAN, 500 kbit/s, 11-bit identifiers, ISO 15765-4 (STANDARD).
- Mode 01 requests sent to 7E0 or broadcast reach the ECM; they bypass the TCM. TCM data needs Mode 22 to 7E2 (REPORT, matches the app).
- GMW3110 (GM's standard, 336 pp, Feb 2010) defines slots only, not which module sits in a slot. The 11-bit scheme has no tester ID; the 29-bit `18DB33F1` convention is not used here.
- Mode 22 naming: in GMW3110, `$1A` ReadDataByIdentifier (1-byte DID, reply `$5A`) is mandatory. `$22` ReadDataByParameterIdentifier (2-byte PID, reply `$62`) is **optional**, meant for development. Live data goes through `$2C` + `$AA`. Poll ECM and TCM one at a time: only one physical request is in flight per module.
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

- **Correction:** PID 0x50 is the maximum MAF air flow, not MAP. It says nothing about the manifold sensor. The only standard max-MAP claim is PID 0x4F byte D × 10 kPa, and whether the E38 supports 0x4F is unknown (check the 0x40 bitmap).
- PID 0B is one byte, so it cannot exceed 255 kPa absolute whatever the sensor does. A 2.7 bar sensor reaches 270 kPa, so 0B cannot show the top of its range even unclamped.

### The risk, and the test that settles it (read before trusting boost numbers)
SAE J1979 defines PID 0B as **one byte = kPa directly** (0–255 kPa) (STANDARD). On a stock OS the right decode is `A`, not the
voltage-style formula above. The report's formula only holds if the custom OS deliberately rescales PID 0B so the byte spans
0–5 V. Nobody has shown that. A wrong guess here is a roughly 20 % error in the displayed boost, which on a tune is a safety issue.

Sensor-side facts from the research (section 3.3 of the research file):
- The line `62.5 × V − 11.25` and the byte form `(A/255) × 312.5 − 11.25` are the same line. 312.5 is kPa across the whole 5 V span, not kPa per volt. Byte resolution is about 1.23 kPa.
- 5 V gives 301.25 kPa, beyond the sensor's assumed 0.5–4.5 V window (270 kPa). Above about ADC count 229.5 the sensor is out of range (open, shorted to 5 V, or a supply error). A logger should **flag** that, not display it.
- Below 0.18 V the formula goes negative. The app clamps at 0.
- The 0.5–4.5 V range is **unsourced**. No datasheet for the PFEFI-MAP2 or Bosch 0261230262 was retrievable. The retailer's "up to 1.9 bar" conflicts with 2.7 bar absolute.

Key-on engine-off check (atmospheric pressure, about 101 kPa at sea level):

| Raw byte shown | Meaning |
|---|---|
| about `0x65` (101) | PID 0B is plain kPa. The 2.7 bar formula is **wrong** for this OS; use `A`. |
| about `0x5C` (92) | PID 0B is the report's rescaled form. The new scaling is right. |

Then compare the decoded value with PID 0133 (baro) and a mechanical gauge under boost. Until done, treat boost from 010B as unconfirmed.
Also unproven: the 151.3 kPa cap. **Research found no primary source for it.** It is not explained by the one-byte 255 kPa limit, and on the 2.7 bar line it equals 2.60 V, not a byte or ADC boundary. Whether the E38 stops advancing the VVE table there is UNVERIFIED. Forum reports of readings stalling near 105 kPa are secondary and unverified.
Do not trust PID 0B above the value measured on the car. Cross-check with baro (PID 0133) and a gauge.

## 3. T43 / 6L80E transmission

- Ratios (**secondary sources**: T2 reproduces GM's specs, ATSG rounds them; the GM service manual was not retrievable): 1st 4.027, 2nd 2.364, 3rd 1.532, 4th 1.152, 5th 0.852, 6th 0.667, reverse about 3.06.
  The app uses these to imply the gear from turbine/output speed (`live.py`).
- Verified in code: `22199A` current gear (7E2, VERIFIED-CAR); `221941` input shaft speed and `221942` output shaft speed,
  both `((A*256)+B)/4` or `×0.125` (two formulas in the list; see `scanner/t43_pids.py` for how the app picks).
- Driveability notes (REPORT, tuning folklore not tested here):
  - TCC is available in 2nd–6th, with 20–80 rpm slip control (ATSG, secondary).
  - The T43 is the TCM inside the transmission (GM bulletin, primary). Five multi-disc clutches and one sprag.
  - Not supported by any source found: a '1-8-9' clutch chart for the 6L80, and the pressure-control solenoid current range. Do not use 4L60-E figures.
  - Stall on deceleration with a high-stall converter: keep TCC desired-slip tables active in low gears and disable low-speed lockup.
  - Power drop on 2-3 upshift under boost: ECM upshift torque management retards timing, up to about a second. Report suggests
    a factor of 0.5–0.7 and more line pressure. A tune change; confirm in the calibration tool, not here.

## 4. FPCM and the fuel system

- **Research:** the only GM FPCM text found is for a 2011 Saab 9-4X, a different vehicle. Nothing ties an FPCM to 7E3 on a VE. The GMLAN message ID, readable data and failure symptoms for a VE were not found.

- FPCM takes a target pressure from the ECM over CAN and drives the pump by PWM. Sensor is in-line. Header 7E3 (REPORT, not confirmed).
- Report's scenario: at 9 psi boost on E85, rail pressure falls 58 psi → 40 psi against a 50.7 psi minimum. Causes given: voltage drop in
  14 AWG wire at 35–45 A, E85's higher volume demand, and the returnless PWM reaching 100 %.
- Treat the numbers as **UNVERIFIED**: the ">3 V drop" and "14.2 V → under 11 V" figures are not derived from a wire length; the
  conductor resistance is never stated. The mechanism (undersized harness, duty pinned at 100 %) is plausible and cheap to check:
  log pump duty and supply voltage together under load.
- What the app can log for it, all unconfirmed on the car:
  - `221471` FPCM duty cycle (7E3), `A × 0.392157` %: in the `gm-report-extras` pack.
  - `0123` fuel rail pressure (kPa ×10), `0122` rail pressure relative to manifold (×0.079), `010A` low-side pressure (×3), `0142` module voltage, `221141` ignition feed voltage: in the Generic OBD-II packs or the catalogue.

## 4a. Service IDs: what a read-only tool must never send

Block by the service byte at the transport layer, not by convention. From GMW3110 Table 6:
`$04` ClearDiagnosticInformation; `$10` InitiateDiagnosticOperation; `$27` SecurityAccess (bad keys lock the ECU out for a delay);
`$28` DisableNormalCommunication; `$2D` DefinePIDByAddress; `$34`, `$36` RequestDownload and TransferData; `$3B` WriteDataByIdentifier;
`$A2`, `$A5` programming flow; `$AE` DeviceControl; `$23` ReadMemoryByAddress (a memory-dump primitive, no logging use).
Also block J1979 Mode `$08` (general knowledge, not read from a primary text).

The UDS numbers `$2E`, `$14`, `$11`, `$31`, `$35` are not GMLAN services in GMW3110; `$11` and `$35` appear only as return codes. Block them anyway.
`$2C` (with `$AA`) is the one allow-listed service that changes ECU state (volatile logging setup); gate it behind an explicit user switch.

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

## Verify-on-car additions (from research)

7. Check whether the E38 answers PID 0x40 and 0x4F, and what 0x4F byte D returns with the 2.7 bar sensor fitted.
8. Confirm the sensor's real voltage range with a multimeter at key-on, engine off (about 0.5 V at vacuum, 4.5 V at full boost).
9. Confirm which module answers on 7E2 and 7E3 by reading the supported-ID bitmaps on each.

## Open questions (added)

- Does the 6L80E's pressure-control solenoid current range match anything published? (no primary source yet)
- Is the GMW3110 revision on the car the same as the mirror read? (mirror is third-party)

## Changelog

- 2026-11-07 (later): merged the primary-source research (`docs/research/gm-primary-sources.md`). Corrections: 0x50 is max MAF not MAP;
  7E2 TCM and 7E3 FPCM are conventional, not confirmed by any primary source; 6L80 ratios and TCC details are secondary;
  the 151.3 kPa cap has no source. Added the `$1A`/`$22` naming, the service-byte deny-list, and 5 V out-of-range flagging.
- 2026-11-07: file created. Added 2.7 bar MAP decode (core v0.4.1), `gm-report-extras` pack, the conflict register and the PID 0B scaling test.
  Primary-source research agent still running; its file is not merged.
