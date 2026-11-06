# What came from the Torque Pro extraction, and what did not

Source: `~/torque-pro-main/5-extracted-data` (static analysis of Torque Pro 1.12.108). Everything that was taken went
through the app's own Torque CSV reader (`scanner/torque_csv.py`), so only Mode 01 and Mode 22 reads with a plain
A-to-D equation can ever be saved. Every row stays marked "not confirmed on a real car".

Shipped in core v0.4.0 (two new packs, under Settings > GM and Holden PID lists):

| Pack | Rows | Source |
|---|---:|---|
| Ford incl. PowerStroke | 44 | `manufacturer-pids/ford_incl_powerstroke.csv` + `ford_secondary_table.csv`, built by `tools/build_torque_packs.py` in the core repo |
| Generic OBD-II: more | 14 | Standard SAE J1979 Mode 01 readings in `torque_builtin_sensors.csv` that neither the catalogue nor the existing Generic OBD-II pack had: lambda B1S3, B1S4, B2S3, B2S4; O2 current B1S3 to B2S4 (this is the V8's second bank); driver demand, actual and reference torque; ECU odometer |

## Not taken, and why

| Item | Result |
|---|---|
| GM / Pontiac / Opel / Vauxhall (87) | Nothing to add. All 87 rows were already in `torque_gm_predefined.csv` with identical equations. |
| Torque built-in sensors (202) | 87 are Mode 01: 14 added above, the rest were already in the catalogue or the base Generic pack, or have bit-packed equations (MAF A, boost command, DPF, NOx, exhaust pressure) that the reader cannot express. The other 115 are not PIDs: 96 are values Torque computes itself (MPG, trip distance, HP estimate, ...) and 9 are phone sensors (GPS, accelerometer). They need app-side code, not a pack. |
| Ford rows dropped (19 of 63) | 14 name a module the app cannot address (TCM, ABS, 726 tyre pressure, C410F1); sending them to the broadcast address would read the wrong module, so they are left out. 1 uses a function call in its equation. 4 repeat a PID already in the pack (the app keeps one reading per PID). |
| Chrysler / Dodge / Jeep / Mercedes (3) | Two are Mode 21 on a module the app does not address; one has the header `7E0,3E01`. Not worth a pack. |
| Prius Gen 2, Gen 3, PHV; Orion BMS; Emerald M3D | Most rows use more than four reply bytes (letters E to R), `VAL{}` references or `{A:7}` bit syntax, or Mode 21 on 7E2 / 7E3. Only 30 or so rows per file would load, and the Toyota-style pack is waiting for the owner's own CSV, so these were not added. |
| `j1939_spn_database.csv` (3,493) | Heavy-truck fault codes; not part of this change. |
| `torque_widgets.json` | The app already has Text, Digital gauge, Graph, Histogram and Analogue. Torque also has half dials, an on/off indicator, status widgets (drive cycle, emission monitors, fuel and air status), a compass, pitch and roll, an acceleration widget and a clock. None added. |

## Known limit

One PID is one reading in this app. A Torque file that reads four values out of one reply (the Ford and Prius ABS
wheel speeds) keeps only the first.
