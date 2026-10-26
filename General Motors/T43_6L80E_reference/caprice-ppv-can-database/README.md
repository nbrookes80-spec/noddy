# Chevrolet Caprice PPV (2011-2017) high-speed CAN database

Decoded CAN messages from a **2014 Chevrolet Caprice PPV** (Holden-built, GM Zeta platform):
6.0 L L77 V8 with **E38 ECM**, **6L80E** transmission with internal **T43 TCM**.
Bus: GM high-speed GMLAN, **500 kbps**, 11-bit IDs, OBD-II pins **6 (CAN-H) and 14 (CAN-L)**.
Much of it should carry over to the Holden VE/VF Commodore, Pontiac G8, Chevrolet SS and other
2008-2015 GM cars with E38/E67 and 6L80E/T43.

## Files

| File | What it is |
|---|---|
| `can_ids.csv` | Every ID seen on the bus (about 76), with rate, sender, decoded bytes, confidence and notes |
| `caprice_ppv.dbc` | The decoded signals in DBC format (SavvyCAN, cantools, Vector tools, etc.) |

## Confidence levels

- **verified**: checked against an independent reading (dash gauge, scan tool, known value) or a deliberate test
- **likely**: layout matches a source or clear log behavior, not independently confirmed
- **guess**: plausible but unconfirmed
- **none**: seen on the bus, meaning unknown

## How it was decoded

Listen-only logging of the car with marked actions (pedals, shifter, paddles, lights, doors, HVAC),
fuse-pull tests to identify which module sends each ID, and comparison against public sources:

- GM Worldwide Engineering Standard **GMW8762** (PPEI, 2011): frame names and byte layouts for many powertrain/chassis frames
- comma.ai **opendbc** (`gm_global_a_powertrain.dbc`)
- **pcmhacking.net** forum threads on E38/T43 CAN (send/receive ID lists)
- LS1Tech CAN broadcast threads

## Highlights

- `189` / `199`: TCM to ECM torque-limit requests used for shift torque management.
  12-bit limit, Nm = raw x 0.5 - 848 (0xFFF = no limit), 2-bit rolling counter, check word.
  Both frames carry the same limit during a cut.
- `1F3`: paddle taps (1 = +, 2 = -).
- `1F5`: current gear (1-6, 13 N, 14 R, 15 P) and shifter range (P/R/N/D/L).
- `0F9` / `19D`: actual gear ratio, output shaft speed and turbine speed.
- `3FB`: ethanol content (flex fuel). `4D1`: oil temperature/pressure, fuel level.
- `772` / `77F`: ECM / TCM trouble-code broadcast frames.

## License and credit

Licensed under **CC BY 4.0** (see `LICENSE`). You may use, share and adapt this data, including commercially,
as long as you give credit. Please credit: **aisom02 (github.com/aisom02/caprice-ppv-can-database)**.

## Disclaimer

Provided as-is for research and education. Transmitting on a vehicle bus can cause faults,
unexpected behavior or damage; listen-only is safe. Verify every signal on your own car.
