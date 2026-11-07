# GM powertrain diagnostics: primary-source research

Target: 2011 Holden Calais (VE Series II), L77 6.0 L V8, E38 ECM, 6L80E with T43 TCM, aftermarket 2.7 bar MAP (Proflow PFEFI-MAP2), returnless fuel with FPCM. App: Tuner Tool Pro, ELM327-class adapter, ISO 15765-4 CAN 500 kbit/s 11-bit.

Research date: 2026-11-07. Reading and writing this one file only. Nothing was sent to any vehicle.

## 0. How to read this document

Every claim carries a source tag. The tag tells you how much weight to give it.

| Tag | Meaning |
|---|---|
| **[P]** | Primary: the document is written by the body that owns the claim (GM engineering standard, GM service bulletin, ELM Electronics datasheet, SAE/ISO catalogue entry, US law text, ACCC). |
| **[P-mirror]** | Primary document, but I read it from a third-party copy because the owner does not publish it free. The text is GM's; the hosting is not. |
| **[V]** | First-party tool or vendor documentation (CSS Electronics, HP Tuners, EFI Hardware). Owns its own tool behaviour, does not own the standard it summarises. |
| **[S]** | Secondary, unverified: forum, retailer listing, wiki, third-party manual publisher. Never used as the only basis for a claim. |

"No primary source found" means exactly that. I did not fill gaps from memory unless the text says "general knowledge, not verified".

### Source register

| ID | Source | URL | Tag | Notes |
|---|---|---|---|---|
| G1 | GMW3110-2010, "General Motors Local Area Network Enhanced Diagnostic Test Mode Specification", Feb 2010, 336 pp, (c) General Motors | https://raw.githubusercontent.com/rusefi/rusefi_documentation/master/OEM-Docs/GM/gmw3110-2010.pdf | P-mirror | Full text read via pdftotext. Page numbers below are the document's own "Page N of 336". |
| E1 | ELM327 datasheet (file label ELM327DSJ, 94 pp), Elm Electronics | https://www.elmelectronics.com/wp-content/uploads/2016/07/ELM327DS.pdf | P (for ELM327 behaviour) | Read via pdftotext. |
| B1 | GM service bulletin "2006 Corvette: 6L80 Automatic Transmission (RPO MYC)", (c) General Motors | https://www.corvetteactioncenter.com/tech/knowledgebase/pdf-351.html | P-mirror | GM text, hosted by a Corvette site. |
| B2 | GM Service Bulletin 16-NA-019, Aug 2016, "Transmission Adaptive Functions" (8L90/8L45 only) | https://static.nhtsa.gov/odi/tsbs/2016/SB-10081880-5448.pdf | P | Hosted by NHTSA. Not a 6L80 document. |
| W1 | Saab WIS Online, 2011 9-4X, "Data Link Communications Description and Operation" (GM Global A platform) | https://saabwisonline.com/9-4x/2011/3-electrical-system/bus-and-diagnostics-communication/technical-description/data-link-communications-description-and-operation | P-mirror | GM-group service information, different vehicle. |
| W2 | Saab WIS Online, 2011 9-4X, DTC P025A and DTC P1255/P064A (FPCM) | https://saabwisonline.com/9-4x/2011/2-engine/engine-management-and-fuel-system-v6/fault-diagnosis-diagnostic-trouble-codes/dtc-p025a and .../dtc-p1255-or-p064a | P-mirror | GM-group service information, different vehicle. |
| J1 | SAE J1979_201702 catalogue entry | https://saemobilus.sae.org/standards/j1979_201702-e-e-diagnostic-test-modes | P (abstract only) | Standard text is paywalled and was not read. |
| J2 | SAE J2534-1 catalogue entry | https://saemobilus.sae.org/standards/j25341_200411-recommended-practice-pass-thru-vehicle-programming | P (abstract only) | Paywalled. |
| R1 | 40 CFR 86.1808-01, via Cornell LII | https://www.law.cornell.edu/cfr/text/40/86.1808-01 | P | |
| R2 | 42 U.S.C. 7522 (Clean Air Act s.203), via Cornell LII | https://www.law.cornell.edu/uscode/text/42/7522 | P | |
| R3 | CARB notice of public hearing, 13 CCR 1968.2 (OBD II), 2004 rulemaking | http://ww2.arb.ca.gov/sites/default/files/barcu/regact/obd02/notice.htm | P | Lists standards incorporated in 2004; editions are old. |
| R4 | ACCC, Motor Vehicle Information Scheme | https://www.accc.gov.au/focus-areas/motor-vehicle-information-scheme-mvis | P | |
| H1 | HP Tuners TDN app, "Supported Controllers" | https://files.hptuners.com/tdn/app/Content/Supported_Controllers.htm | V | |
| C1 | CSS Electronics OBD2 PID table | https://www.csselectronics.com/pages/obd2-pid-table-on-board-diagnostics-j1979 | V | Tool vendor summarising J1979. |
| C2 | Wikipedia, "OBD-II PIDs" | https://en.wikipedia.org/wiki/OBD-II_PIDs | S | Cross-check only. |
| M1 | EFI Hardware (AU distributor), Delco 2 Bar MAP H-MAP2 technical diagram | https://efihardware.com/download/113/H-MAP2 | V | Distributor drawing for a Delco 2 bar part, not Proflow. |
| M2 | Retailer listings for Proflow PFEFI-MAP2 / Aeroflow AF49-1559 | https://fastlanespares.co.nz/products/proflow-gm-map-sensor-2-7-bar-gen-4-ls2-ls3-lsa-3-pin (listing text seen through search; the page itself returned HTTP 429 on direct fetch) | S | |
| T1 | ATSG "Hydra-Matic 6L80" manual demo, (c) ATSG 2007 | https://krutilvertel.com/pdf/demo/motorist/service-manual-gm-6l80-demo.pdf | S (professional publisher, not GM) | Only the demo pages are public. |
| T2 | xlr-net.com, "2006-2009 Cadillac XLR-V: 6L80 Transmission Specifications" | https://www.xlr-net.com/knowledgebase/article/2006-2009-cadillac-xlr-v-6l80-transmission-specifications-18.html | S (reproduces GM service-manual specs) | |

---

## 1. CAN addressing

### 1.1 What GM's own standard defines

All from G1.

| Fact | Detail | Where |
|---|---|---|
| OBD/EOBD ID range | `$7DF` functional request; `$7E0..$7E7` physical requests for "OBD ECU #1..#8"; `$7E8..$7EF` matching physical responses. Pairing is request + 8: #1 `7E0`/`7E8`, #2 `7E1`/`7E9`, #3 `7E2`/`7EA`, #4 `7E3`/`7EB`. | Table 10, p.26 |
| The standard assigns slots, not functions | Table 10 says only "OBD ECU #1" through "#8". It never says which module is the ECM, TCM or anything else. | Table 10, p.26 |
| Enhanced diagnostics may share the OBD IDs | An emissions-related ECU "may choose to use the OBD/EOBD diagnostic CAN Identifiers to also support enhanced diagnostics." Enhanced UUDT responses then use `$5E8..$5EF` (ECU #1 -> `5E8`, #3 -> `5EA`, #4 -> `5EB`). | 4.4.4.1, Table 11, pp.26-27 |
| Native GMLAN diagnostic IDs | Physical request `$241..$25F`; UUDT response `$541..$55F`; USDT response `$641..$65F`; `$240/$540/$640` reserved. Low byte is a per-node offset (`$646` -> UUDT `$546`, request `$246`). | Table 8, p.24-25; 4.4.4, p.25 |
| Functional addressing | AllNode request CAN ID `$101` with an extended-address byte. `$FE` = all functional systems, `$FD` = gateways. Example frames: `$101 $FE $01 $3E` (TesterPresent), `$101 $FE $03 $22 $00 $0C` (RPM). | Table 8 p.24; Table 26 p.39; 8.15 TesterPresent example p.176; 8.6.5 examples p.110-111 |
| Physical vs functional is set by the CAN ID | "The diagnostic CANId in a request message also determines the type of addressing used". All responses are physical. | 4.4 intro, 4.5, pp.22, 28 |
| Normal addressing for physical and OBD IDs | USDT with normal addressing: PCI starts in data byte 1. Extended addressing (AllNode) puts the EA byte first and PCI second. | 4.5.1, Tables 14-15, p.28-29 |
| Tester rules | Only one physically addressed request may be in process at a time; no new physical request while a functional request's response is in process; functional requests that expect a response are not allowed while any request is in process; wait at least 30 ms after a functional request before the next functional request. | 4.3.1 rules 1-6, p.19-20 |
| Diagnostic addresses are separate from CAN IDs | Each ECU has a one-byte "diagnostic address" (read with `$1A`, DID `$B0`). "There is no numerical relationship between the ECU Diagnostic Address and the Diagnostic CAN Identifiers." Ranges: engine controllers `$10..$17`, transmission controllers `$18..$1F`. The spec's own example shows ECM `$11`, TCM `$18`. | 4.4.4 note p.25; Fig. 8 p.39; App. D, Table D1, p.317 |
| Tester identification | The GMLAN 11-bit scheme has no tester source-address field. The tester is identified only by which request ID it uses. I found no "tester ID" value in G1. | Tables 8, 10, 13 |

### 1.2 The 29-bit contrast (ISO 15765-4), for context only

E1 (p.40-41) describes the ISO 15765-4 29-bit case: priority byte `18`, type byte `DB` for functional / `DA` for physical, receiver `33` for functional requests, transmitter (tester) `F1`. That gives the familiar `18 DB 33 F1`. This is the only "tester ID" convention I found in a primary source, and it applies to 29-bit CAN, which your 11-bit E38 does not use.

### 1.3 Questions asked, answered

| Question | Answer | Source / status |
|---|---|---|
| 7E0/7E8 = ECM? | Slot #1. E1 says of a header-on reply from `7E8`: "ECU#1 was the one responding" and "it is 7E0 to talk to the 7E8 device". G1 examples use `7E0`/`7E8` with J1979 PID `$0C` (RPM) and `$05` (coolant temp). Strongly consistent with ECM, but neither document says "7E0 is the ECM". | E1 p.41; G1 Tables 85-86 p.110-111. Function assignment: **no primary source found** for the VE; conventional reading only. |
| 7E2/7EA = TCM? | Slot #3 per G1 Table 10. Whether the VE Series II T43 answers there: **no primary source found.** HP Tuners lists T43 as a supported GM TCM but gives no CAN ID. | G1 Table 10; H1 |
| 7E3/7EB = FPCM? | Slot #4 per G1 Table 10, nothing more. **No primary source supports "FPCM on 7E3".** Nothing I read says the FPCM is an OBD-ID module at all. Treat the claim as unverified. Safe approach: do not assume; discover it with a functional `01 00` and watch which IDs answer. | G1 Table 10; see section 7 |
| GMLAN vs OBD-II on the same bus | Same wires. HS-GMLAN is two-wire 500 kbit/s, on DLC pins 6 (+) and 14 (-) (9-4X; the VE uses the same J1962 pins by convention but I have no VE document). Legislated OBD (J1979) and GMW3110 enhanced services share the `7Ex` IDs on emissions-related modules; other modules use `$24x/$64x/$54x`. | G1 4.4.4.1; W1 |
| Is there a GM-specific functional ID besides 7DF? | Yes, `$101` with EA `$FE`, but it is a GMLAN-native request. A read-only OBD app has no reason to use it, except that G1 notes `$101 $FE $01 $3E` as the functional TesterPresent. | G1 4.4.3, 8.15 |

### 1.4 ELM327 mapping (E1)

| Need | ELM327 command | Source |
|---|---|---|
| ISO 15765-4, 11-bit, 500 kbit/s | `AT SP 6` ("6 - ISO 15765-4 CAN (11 bit ID, 500 kbaud)") | E1 p.25 |
| Send to ECM physically | `AT SH 7E0` ("it is 7E0 to talk to the 7E8 device"); `AT SH 7DF` for functional | E1 p.24, p.41 |
| Listen to one responder | `AT CRA 7E8` | E1 p.15 |
| Raw frames, no PCI handling | `AT CAF0` (with formatting on, "messages with invalid PCI bytes will be ignored") | E1 p.13-14 |
| Extended-address tester (GMLAN `$101`) | `AT CEA hh` (inserts hh as the first data byte of every message sent) | E1 p.14 |

Implication, my inference from the CAF text and G1 4.5.1.2: UUDT frames from service `$AA` have a DPID byte where a PCI byte would be. With `AT CAF1` the ELM327 may discard them. A DPID reader needs `CAF0` and `CRA 5E8` (or monitor mode). Not tested.

---

## 2. SAE J1979 Mode 01 PIDs for a boosted V8

The J1979/ISO 15031-5 text is paywalled (J1: catalogue entry only). I could not read it. The formulas below come from two independent non-owner summaries that agree (C1 and C2, bytes A,B,C,D) and, for 0x05 and 0x0C, are independently confirmed inside GM's own standard G1. They are consistent with each other but, strictly, **no free primary text of J1979 was read.**

| PID | Name | Bytes | Formula | Range (formula) | Notes |
|---|---|---|---|---|---|
| 0x0B | Intake manifold absolute pressure | 1 | `A` kPa | 0..255 | 1 kPa per bit, saturates at 255 kPa abs. |
| 0x0C | Engine speed | 2 | `(256*A + B) / 4` rpm | 0..16383.75 | Confirmed in G1 Table 85 (p.110): request `03 22 00 0C`, response `05 62 00 0C 0B B8` = 0x0BB8 = 3000 / 4 = 750 rpm. |
| 0x0D | Vehicle speed | 1 | `A` km/h | 0..255 | |
| 0x0E | Timing advance | 1 | `A/2 - 64` deg BTDC | -64..63.5 | C1 prints max 64; formula gives 63.5. |
| 0x0F | Intake air temperature | 1 | `A - 40` degC | -40..215 | |
| 0x11 | Throttle position | 1 | `100*A/255` % | 0..100 | |
| 0x33 | Absolute barometric pressure | 1 | `A` kPa | 0..255 | |
| 0x43 | Absolute load value | 2 | `100*(256*A + B)/255` % | 0..25700 | Normalised air mass per intake stroke; can exceed 100 % on boosted engines. The J1979 definition text was not read. |
| 0x4F | Maximum values for equivalence ratio, O2 voltage, O2 current, MAP | 4 | A = max FAER; B = max O2 V; C = max O2 mA; **D x 10 = max MAP kPa** | D: 0..2550 | See below. |
| 0x50 | Maximum value for MAF air flow rate | 4 | `A x 10` g/s; B,C,D reserved | 0..2550 | **Not a MAP value.** |
| 0x52 | Ethanol fuel % | 1 | `100*A/255` % | 0..100 | |
| 0x5C | Engine oil temperature | 1 | `A - 40` degC | -40..215 by formula | C2 prints 210, C1 prints 215. The formula is the same in both. |
| 0x5E | Engine fuel rate | 2 | `(256*A + B)/20` L/h | 0..3276.75 by formula | C2 prints 3212.75, C1 prints ~3277. Flag, formula agrees. |
| 0x00/0x20/0x40/0x60 | Supported-PID bitmaps | 4 | bit-encoded `[A7..D0]` = next 32 PIDs (C2) | | E1 p.41 shows a `01 00` reply `41 00 BE 3F B8 13` as the bitmap form. Use these, not guesswork, to learn which of the PIDs above the E38 supports. |

### 2.1 What 0x4F and 0x50 say about MAP range

- 0x4F byte D, times 10, is the largest MAP the ECU says it can report, in kPa. Resolution is 10 kPa. It is the only standard PID that states the MAP range an ECU claims.
- 0x50 is the maximum MAF air flow, not MAP. It tells you nothing about the manifold sensor.
- Whether the E38 supports 0x4F at all, and what D it returns with a 2.7 bar sensor on a stock or custom OS, is **unknown: no primary source found.** Read the 0x40 bitmap and query it; do not assume.
- Because PID 0x0B is one byte, it cannot exceed 255 kPa absolute no matter what the sensor does. A 2.7 bar sensor reaches 270 kPa at full range (section 3), so 0x0B is structurally unable to show the top of the sensor range even if the ECU were unclamped.

---

## 3. MAP sensor scaling

### 3.1 What I could and could not find

| Item | Finding | Tag |
|---|---|---|
| GM 1-bar, 2-bar, 3-bar transfer functions | **No GM primary datasheet or service-manual table found.** | |
| Proflow PFEFI-MAP2 datasheet | **No Proflow/Holley datasheet found.** Retailer text says: 2.7 bar, Gen 4 LS2/LS3/LSA, 3-pin, replaces Bosch 0261230262, plug PFEFI-027, and "up to 1.9 BAR" for universal use. That last figure does not match 2.7 bar absolute (270 kPa abs = 1.69 bar gauge), so the listing is internally unclear. One listing of the Aeroflow equivalent calls it both 2.7 and 2.9 bar. | S (M2) |
| Bosch 0 261 230 262 datasheet | **Not found.** Search surfaced Bosch datasheets only for other part numbers (e.g. 0 261 230 112, 145); the host (finjector.com) returned HTTP 403 when I tried to open one, so none was read. | |
| A 2-bar Delco calibration | EFI Hardware H-MAP2 drawing: pin B output "0 V to 5 V", 0.30 V at 20 kPa, 4.80 V at 200 kPa, 2.325 V at atmospheric. | V (M1) |
| 3-bar GM 12223861 | A seller listing quotes about 1.1 kPa at 0 V and 315.5 kPa at 5 V (slope about 62.9 kPa/V). Seen only in a search snippet; page not opened. | S |

### 3.2 Algebra from the vendor 2-bar drawing (M1), derived by me

Linear through (0.30 V, 20 kPa) and (4.80 V, 200 kPa):

- slope = (200 - 20) / (4.80 - 0.30) = 40 kPa/V
- kPa = 40 * V + 8
- Check at atmosphere: 40 * 2.325 + 8 = 101 kPa. OK, consistent with the 2.325 V label.

So this 2-bar part is not a 0.5-4.5 V sensor. Do not reuse its numbers for the 2.7 bar part.

### 3.3 Your proposed 2.7 bar scaling: `kPa = V*62.5 - 11.25` and `kPa = (A/255)*312.5 - 11.25`

I checked this numerically.

**Does it describe a 0.5-4.5 V sensor spanning 20-270 kPa?** Yes.

- Two-point fit: slope = (270 - 20) / (4.5 - 0.5) = 250 / 4 = **62.5 kPa/V**.
- Offset = 20 - 0.5 * 62.5 = 20 - 31.25 = **-11.25 kPa**.
- Cross-check at the top: 4.5 * 62.5 - 11.25 = 281.25 - 11.25 = **270 kPa**. 

**Is the 8-bit form the same line?** Yes, if the 8-bit count `A` is the fraction of a 5.000 V reference.

- V = 5 * A / 255
- V * 62.5 = (A / 255) * 5 * 62.5 = (A / 255) * **312.5**
- So 312.5 is `62.5 kPa/V * 5 V`, i.e. kPa across the **whole 0-5 V span**, not kPa per volt.

| Input | Via `V*62.5 - 11.25` | Via `(A/255)*312.5 - 11.25` | Comment |
|---|---|---|---|
| 0 V (A = 0) | -11.25 kPa | -11.25 kPa | Negative: below sensor range, a fault zone. |
| 0.18 V | 0 kPa | | Zero-crossing. |
| 0.5 V (A = 25.5) | 20.00 kPa | 20.00 kPa | Lower end of the assumed span. |
| 1.80 V (A = 91.8) | 101.3 kPa | 101.3 kPa | Atmospheric. |
| 2.60 V (A = 132.6) | 151.3 kPa | 151.3 kPa | Value of the "151.3" figure on this scale, see section 4. |
| 4.26 V (A = 217.5) | 255.0 kPa | 255.0 kPa | Where PID 0x0B saturates. |
| 4.5 V (A = 229.5) | **270.00 kPa** | **270.00 kPa** | Upper end of the assumed span. |
| 5.0 V (A = 255) | **301.25 kPa** | **301.25 kPa** | Beyond the rated span. |

Quantisation of the 8-bit form: 312.5 / 255 = 1.2255 kPa per count, so a byte cannot resolve better than about 1.2 kPa.

**Inconsistencies to flag**

1. The arithmetic is internally consistent. The two formulas are the same line.
2. 312.5 is easy to misuse. Applied per volt, `312.5*V - 11.25` gives 1395 kPa at 4.5 V. Name the constant `FULL_SCALE_KPA` or keep it with the `/255`.
3. 5 V gives 301.25 kPa, 31 kPa above the 270 kPa the assumed 4.5 V endpoint represents. An ADC count above about 229.5 means the sensor is out of its rated 0.5-4.5 V window (open, short to 5 V, or ratiometric supply error). A logger should flag it, not display 301 kPa.
4. `-11.25` produces negative kPa below 0.18 V. Clamp or flag.
5. The whole line is only valid if the sensor really is 0.5-4.5 V over 20-270 kPa. I found no datasheet that confirms this for the PFEFI-MAP2 or Bosch 0261230262. It is an assumption.
6. Ratiometric: Bosch-style MAP sensors scale with their supply. If the ECM reference is not exactly 5.000 V the slope shifts. Not sourced for this part.
7. Two ceilings stack: PID 0x0B (255 kPa) and the sensor (270 kPa). They differ by 15 kPa.
8. 270 kPa absolute at 101.3 kPa ambient is 168.7 kPa gauge = 1.69 bar = 24.5 psi of boost. At 255 kPa it is 153.7 kPa gauge = 22.3 psi.

---

## 4. The "151.3 kPa cap" on a stock E38 OS (PID 0x0B)

| Question | Answer |
|---|---|
| Is a single-byte limit the explanation? | No. The J1979 byte limit for PID 0x0B is 255 kPa (C1, C2). 151.3 is well below that. A byte cannot by itself explain a cap at 151.3. |
| Is "151.3 kPa" documented in any primary source? | **No primary source found.** I searched the web for it alongside GM, HP Tuners and EFILive terms, and read EFILive release-note search results. The only mentions of MAP clipping are forum posts, and none I saw says "151.3". I did not read the full HP Tuners or EFILive manuals (not publicly retrievable). Treat the number as unverified. |
| What do forums say? | Forum threads (HP Tuners, LS1Tech) say a stock OS needs MAP-axis tables shifted or a 2/3-bar custom OS to use a 2 or 3 bar sensor, and report readings that stall near 105 kPa (secondary, unverified). They do not establish a 151.3 limit. |
| What does the number correspond to on your line? | On `62.5*V - 11.25` it is 2.60 V (A = 132.6). That is not a power-of-two, byte or ADC boundary, so I cannot explain it from the algebra. If the 151.3 figure is real, it probably comes from the stock 1-bar sensor transfer function in the OS calibration, but that is a guess: **no primary source found.** |
| What to do in the app | Do not trust PID 0x0B above the figure you measure. Cross-check against `0x4F` D (if supported) and against a key-on, engine-off reading versus PID `0x33` baro. A custom OS or a tuner-supplied enhanced MAP PID may be needed above the cap; the PID IDs are not in any primary source I found. |

---

## 5. GM enhanced diagnostics (GMW3110 / GMLAN)

All from G1.

### 5.1 Architecture

- Two message types. **USDT** (segmented, may be multi-frame, ISO 15765-2 style PCI) and **UUDT** (always a single unsegmented frame, no PCI, first byte is a message number). All requests and all negative responses are USDT. Positive responses may be either, per service (4.1, p.17).
- PCI byte (Table 17, p.29): `0x0n` single frame (n = data length), `0x1n nn` first frame, `0x2n` consecutive frame, `0x3n` flow control.
- Positive response service ID = request service ID + `0x40`. This holds in every table I read: `$1A` -> `$5A` (Table 70), `$22` -> `$62` (Table 82), `$2C` -> `$6C` (Table 116).
- Negative response (Table 40, p.70): `7F <requestServiceId> <returnCode>`; for return code `$E3`, two extra bytes. Example on the wire (Table 41, p.72): request `02 27 01` on `$241`; reply `03 7F 27 11` on `$641`.

| Return code | Meaning (G1 section 7.2) |
|---|---|
| `$11` | ServiceNotSupported (only for physically addressed requests; functional requests are silently ignored) |
| `$12` | SubFunctionNotSupported-InvalidFormat |
| `$22` | ConditionsNotCorrectOrRequestSequenceError |
| `$31` | RequestOutOfRange |
| `$35` / `$36` / `$37` | InvalidKey / ExceedNumberOfAttempts / RequiredTimeDelayNotExpired (security access) |
| `$78` | RequestCorrectlyReceived-ResponsePending |
| `$81` | SchedulerFull |
| `$83` | VoltageOutOfRange |
| `$85` / `$89` / `$99` | Programming failure codes |
| `$E3` | DeviceControlLimitsExceeded (+2 bytes) |

### 5.2 `$22` vs `$1A`: the naming in your question needs correcting

| | `$1A` ReadDataByIdentifier | `$22` ReadDataByParameterIdentifier |
|---|---|---|
| Section | 8.4, p.94 | 8.6, p.107-111 |
| Identifier size | **1 byte** DID | **2 bytes** PID (MSB, LSB) |
| Request | `1A DID` | `22 PIDhi PIDlo [PIDhi PIDlo ...]` (multiple PIDs allowed) |
| Positive response | `5A DID data...` | `62 PIDhi PIDlo data... [PIDhi PIDlo data...]` |
| Intended for | static data (ECU ID, VIN, part numbers, diagnostic address DID `$B0`) | development and special tests |
| Data length | set by the DID | 1 to 7 data bytes per PID |
| Table 6 status | Mandatory (M) | **Optional (U): "DRE can decide whether or not to implement"** |

G1 8.6 says `$22` "is not intended to be used in lieu of service `$AA` for manufacturing and/or field service diagnostics". It also says `$22` can fetch J1979 PIDs: send them "with the most significant byte (MSB) of the PID number set to `$00`", e.g. `22 00 0C`.

Unsupported PIDs in a multi-PID `$22` are silently omitted. A physical request where none of the PIDs are supported returns a negative response; a functional request with only unsupported PIDs gets no reply (8.6.1).

SAE J2190 (the older "Enhanced E/E Diagnostic Test Modes", where Mode `$22` originates): the standard was **not read.** I make no claim about it.

E1 p.40 (Setting the Headers) adds: the PIDs used with mode 22 "are usually proprietary to each manufacturer and are generally not published widely."

### 5.3 `7E0` vs `7E2` for a Mode 22 request

- `7E0` = physical request to OBD slot #1, reply on `7E8`. `7E2` = physical request to OBD slot #3, reply on `7EA`. A `$22` request is meaningless without the right target: a given PID number belongs to one module's data dictionary, so `22 xx xx` sent to the wrong ID returns either a negative response (`7F 22 31`, RequestOutOfRange, when none of the requested PIDs is supported and the request was physical: G1 Table 84) or nothing at all (functional request with only unsupported PIDs: G1 8.6.1).
- Tester rule (G1 4.3.1, rule 1): only one physically addressed request in process at a time. So an app that polls ECM and TCM should serialise the two, not interleave them. Whether the E38 and T43 tolerate overlap in practice is not covered.
- PID numbering for `$22` is manufacturer-defined per module and documented in each module's CTS. **No primary source found** for the E38 or T43 PID lists.

### 5.4 Service list (Table 6, pp.18-19)

Read/write classification is mine, based on each service's section text.

| SID | Name | Table 6 status | Effect | Read-only app? |
|---|---|---|---|---|
| `$04` | ClearDiagnosticInformation | M (ECUs that log DTCs) | **Write:** clears DTC data | Never |
| `$10` | InitiateDiagnosticOperation | C | `$02` disableAllDTCs, `$03` enableDTCsDuringDevCntrl, `$04` wakeUpLinks. Changes DTC logging. | Never |
| `$12` | ReadFailureRecordData | C | Read | Allowed |
| `$1A` | ReadDataByIdentifier | M | Read, 1-byte DID | Allowed |
| `$20` | ReturnToNormalOperation | M | Ends diagnostic session, stops periodic DPIDs, ends `$10`/`$28` states | Allowed, as session clean-up |
| `$22` | ReadDataByParameterIdentifier | U | Read, 2-byte PID | Allowed |
| `$23` | ReadMemoryByAddress | U | Read arbitrary ECU memory, development use, may be security-gated | Avoid; not needed |
| `$27` | SecurityAccess | C2 (M3 for programmable emissions/safety/theft ECUs) | Seed/key unlock | Never |
| `$28` | DisableNormalCommunication | M | Node stops all normal bus traffic; "primary use is to set up a programming event" | Never |
| `$2C` | DynamicallyDefineMessage | C | Defines DPID contents in ECU. Volatile configuration, retained across `$3E` timeout and `$20` (8.10.1). | Not strictly read-only. Needed to use `$AA`. See 5.5. |
| `$2D` | DefinePIDByAddress | U | Maps ECU RAM addresses to a PID. "Only intended for use in engineering development." | Never |
| `$34` | RequestDownload | N/A (boot M) | Start programming transfer, secured | Never |
| `$36` | TransferData | N/A (boot M) | Download / execute blocks | Never |
| `$3B` | WriteDataByIdentifier | C | **Write:** changes ECU data identified by DID | Never |
| `$3E` | TesterPresent | M | Keep-alive; resets the P3 timer; no data change | Allowed; needed for `$AA` scheduler |
| `$A2` | ReportProgrammedState | N/A (boot M) | Reports programmed state | Not needed; avoid |
| `$A5` | ProgrammingMode | M | Enter programming; needs `$28` first | Never |
| `$A9` | ReadDiagnosticInformation | M (ECUs that log DTCs) | Read DTC status/lists; response is UUDT | Allowed |
| `$AA` | ReadDataByPacketIdentifier | C | Read DPIDs: one-shot (`$01`) or periodic (`$02` slow, `$03` medium, `$04` fast, `$00` stop). UUDT responses. | Allowed |
| `$AE` | DeviceControl | C | **Write:** overrides outputs / resets variables | Never |

### 5.5 `$2C` + `$AA` (the live-data path)

- `$2C DPID PIDhi PIDlo ...` packs 2-byte PIDs into a dynamic DPID. Dynamic DPIDs "start with `$FE` and be numbered sequentially backwards". Range `$FE..$90` and `$7F..$01`; `$80..$8F` are reserved for DTC services (8.10.1-8.10.2, Table 114). Each DPID carries at most 7 data bytes (UUDT). Positive response `6C DPID`.
- `$AA <sub> DPID...`: sub-function `$01` one response per DPID; `$02/$03/$04` schedule at slow/medium/fast (default 1000/200/25 ms, "guidelines", per-ECU CTS governs); `$00` stop. Positive responses are UUDT frames whose first byte is the DPID. DPID `$00` is reserved; `$80..$8F` not allowed; `$FF` reserved (Table 192). Periodic scheduling requires `$3E` TesterPresent to keep the scheduler active (8.19 intro, 8.19.1.2).
- Negative response `$81` SchedulerFull if too many DPIDs are scheduled.
- Practical consequence for a read-only logger: `$2C` is the one service on the allow-list that sends configuration. It does not write calibrations or flash, and the spec says it is retained only as DPID definitions, but it is still a state change in the ECU. Document it as "volatile logging setup" and gate it behind a user-visible switch.
- Anecdote (S, LS1Tech thread): a standard-format `$2C` on `7E0` returned `7F 2C 12` for one user while another form worked. Not authoritative; GMW3110 is the format reference.

### 5.6 What a read-only app must never send

Block by service byte (first data byte after PCI) at the transport layer, not by convention.

| Byte | GMW3110 meaning | Why block |
|---|---|---|
| `$04` | ClearDiagnosticInformation | Clears DTCs. Also the SID of J1979 Mode `$04` (clears emissions DTCs and readiness state). The J1979 mode meaning is general knowledge, not read in this session. |
| `$10` | InitiateDiagnosticOperation | `$02` disables DTC setting. |
| `$27` | SecurityAccess | Starts seed/key. Repeated bad keys lock the ECU out for a delay (G1 7.2.5-7.2.7). |
| `$28` | DisableNormalCommunication | Silences the node on the bus; step 1 of programming. |
| `$2D` | DefinePIDByAddress | Development RAM mapping. |
| `$34`, `$36` | RequestDownload, TransferData | Programming. |
| `$3B` | WriteDataByIdentifier | Writes. |
| `$A2`, `$A5` | ReportProgrammedState, ProgrammingMode | Programming flow. |
| `$AE` | DeviceControl | Actuator override. |
| `$23` | ReadMemoryByAddress | Not a write, but a memory-dump primitive; no logging use. |
| J1979 Mode `$08` | Control of on-board system | General knowledge, not verified from a primary text. Block. |

UDS-numbered services you listed that are **not** GMLAN services in GMW3110:

| You listed | GMW3110 reality |
|---|---|
| `0x2E` WriteDataByIdentifier | Not in Table 6. GM's write-by-DID is `$3B`. `$2E` is the ISO 14229 (UDS) number; ISO 14229 was not read here. |
| `0x14` ClearDTC | Not in Table 6. GM's is `$04`. `$14` is UDS/KWP2000 numbering. |
| `0x11` ECU reset | Not in Table 6. In GMW3110, `$11` appears only as a **return code** (ServiceNotSupported). GM's reset-adjacent services are `$20` and the programming path. |
| `0x31` routine control | Not in Table 6. |
| `0x35` | In GMW3110 `$35` is a **return code** (InvalidKey), not a service. |

Still block all of these (and everything not on the allow-list). A stock E38 will answer `7F <sid> 11` to services it does not have, but a UDS-era GM module (not your car) might act on them.

Recommended allow-list for the app: J1979 Modes `01, 02, 03, 06, 07, 09, 0A` (reads), GMLAN `$1A`, `$22`, `$A9`, `$12`, `$AA`, `$3E`, `$20`, with `$2C` behind a user switch. The J1979 mode list is general knowledge; confirm against SAE J1979 before shipping.

---

## 6. 6L80E / T43

### 6.1 What the T43 is and where it sits

| Fact | Source |
|---|---|
| "a Transmission Control Module (TCM) located inside the transmission"; the TCM, shift solenoids, pressure-control solenoids, TFP switches and TFT switch are "all integrated into the solenoid assembly"; the parts "will not be serviced separately". | B1 (GM) |
| The TCM commands "shift solenoids and variable bleed pressure control solenoids" and controls apply/release of the torque converter clutch. | B1 (GM) |
| T43 is listed as a supported GM TCM (alongside T42), E38 listed as a GM ECM. | H1 (HP Tuners) |
| "T43 = the internal TCM of the 6L80/6L90" and part numbers such as 24275873. | Forum posts and vendor listings only: **no primary source found for the designation-to-transmission mapping**; consistent with B1 and H1 but not stated in them. |
| Solenoid layout: one forum thread counts 8 solenoids, 6 PWM and 2 on/off shift solenoids. | S (msgpio.com thread). **No primary source found** for the solenoid count or per-solenoid roles. GM (B1) says only "shift solenoids and variable bleed pressure control solenoids". |

### 6.2 Gear ratios

| Gear | Ratio (T2, GM specs reproduced) | ATSG (T1) rounded |
|---|---|---|
| 1 | 4.027 | 4.03 |
| 2 | 2.364 | 2.36 |
| 3 | 1.532 | 1.53 |
| 4 | 1.152 | 1.15 |
| 5 | 0.852 | 0.85 |
| 6 | 0.667 | 0.67 |
| Reverse | 3.064 | 3.06 |

Your six forward ratios match T2 exactly. T2 is a secondary page reproducing GM service-manual specs. The GM service manual itself was not retrievable. Overall span 4.027/0.667 = 6.04.

### 6.3 Clutch application chart (ATSG, T1 Figure 4)

Names and combinations are ATSG's, not GM's, but they match T2's selective-ring clutch names (1-2-3-4, 3-5-Reverse, 4-5-6, Low/Reverse).

| Range | 1-2-3-4 | 3-5-Rev | 4-5-6 | 2-6 | Low & Rev | Low sprag | TCC |
|---|---|---|---|---|---|---|---|
| Reverse | | X | | | X | | |
| 1st | X | | | | X | holds | |
| 2nd | X | | | X | | | avail. |
| 3rd | X | X | | | | | avail. |
| 4th | X | | X | | | | avail. |
| 5th | | X | X | | | | avail. |
| 6th | | | X | X | | | avail. |

Footnote in the source: TCC is available 2nd through 6th, based on throttle position, fluid temperature and vehicle speed. In manual (M) mode, 1st and 2nd are the same as D1 and D2.

- The six-clutch layout is "five multiple disc clutches ... combine with one mechanical sprag clutch" (B1, GM).
- Your list included a "1-8-9" clutch. **No source I found uses that name for the 6L80.** The 6L80 clutch names are the five above. Treat "1-8-9" as unsupported.

### 6.4 TCC operation and slip

- GM (B1): the four-element converter's pressure plate "provides a mechanical direct drive coupling" when applied. The TCM controls apply and release.
- ATSG (T1, TCC solenoid page): the TCC PC solenoid is a normally-low electronic pressure regulator; the TCM raises current to apply and lowers it to release. The TCM controls a **20-80 rpm** slip between clutch plate and cover; this "ramping" lets the TCC apply at low engine speed in 2nd to 6th. Conditions that can prevent or enable TCC: engine temp, transmission temp, brake switch. Stuck ON / OFF DTCs P0742 / P0741.
- Slip rpm as a measurable value in your app would be engine rpm minus turbine speed. The PID names for turbine/ISS speed on the T43 are **not in any primary source I found.**

### 6.5 Line pressure control and solenoid current

- GM (B1) mentions only "variable bleed pressure control solenoids". No current range.
- ATSG's TCC page describes the principle (current -> pressure) but gives no mA numbers for the line-pressure solenoid.
- Secondary: forum posts say the TCM raises line pressure by modulating the line-pressure PC solenoid. Search-snippet text from an AutoRepairsHQ GM-manual mirror for the 6L-series says a line-pressure solenoid circuit fault makes the TCM command maximum line pressure. I could not open that page (connection refused), so treat as unverified.
- **Pressure control solenoid current and its range for the 6L80E: no primary source found.** A "0.1-1.1 A" figure turned up in a search snippet of a GM-manual mirror page, but that page was for a 4L60-E/4L65-E, not the 6L80, and must not be used.

### 6.6 Adaptive learning

- GM bulletin 16-NA-019 (B2), written for the 8L90/8L45, says wear of apply components changes shift time, and "the transmission control module (TCM) adjusts the pressure commands to the various pressure control (PC) solenoids to maintain the originally calibrated shift timing". It monitors input and output speed sensors during commanded shifts. It calls this "adaptive learning" and says a software update clears the adapts.
- That is GM's own description of the mechanism for the 8-speed. A 6L80E-specific GM text was **not retrieved.** The principle is likely the same (the 6L80 is also clutch-to-clutch with PC solenoids, B1), but that is inference.
- No primary source found for how the 6L80E stores adapt values, for the T43 adapt PIDs, or for the learn procedure.

---

## 7. FPCM (Fuel Pump Control Module), returnless fuel

### 7.1 What a GM FPCM does (GM-group service information, different vehicle)

From W2, 2011 9-4X (GM platform, not a Holden):

- The ECM supplies voltage to the FPCM ("control enable") when it detects ignition on. It stays on for 2 s unless the engine is cranking or running.
- While enabled, the FPCM "supplies a varying voltage to the fuel tank pump module in order to maintain the desired fuel rail pressure".
- The ECM also sends a **serial data message** to the FPCM. P025A sets when that message disagrees with the control-enable state for more than 2 s (Type A). The page does not say what the message contains or whether it is GMLAN CAN.
- P1255 is FPCM driver over-temperature; P064A is FPCM performance (W2). Both Type A.

### 7.2 Commanded over GMLAN? Readable data?

- Whether the VE Series II FPCM is commanded over GMLAN CAN, and what its message ID is: **no primary source found.** W2 says only "serial data message".
- Readable data from the FPCM via diagnostics: **no primary source found.** Nothing I read lists FPCM PIDs, and nothing says the FPCM answers a Mode 01 or `$22` request.
- Aftermarket text says the late-VE pump is PWM controlled with an inline pressure sensor and a commanded pressure held in the FPCM (S, retailer). A Corvette forum thread mentions 400 Hz PWM and HS-GMLAN on the FPCM harness (S, forum). Both unverified.

### 7.3 Failure symptoms

- The GM pages I read give DTC logic, not driver symptoms. The pages for P025A "do not describe drivability or fuel-related symptoms".
- Symptoms such as no-start, hesitation under load, or fuel-pressure loss from a failing FPCM: **no primary source found.** I will not invent them.

### 7.4 "FPCM on 7E3"

**No primary support.** The only primary facts are: (1) G1 Table 10 reserves `7E3`/`7EB` as "OBD ECU #4" with no function; (2) the 9-4X pages show an FPCM that receives a serial message from the ECM. Nothing links them. Discover the topology with the ECM's own supported-ID responses on the car, not from a document.

---

## 8. Rules that bear on a read-only logger

Not legal advice. Only what a read-only logger touches.

| Rule | What it says | Relevance | Tag |
|---|---|---|---|
| SAE J1979 / ISO 15031-5 | The standard for communication between the vehicle's OBD systems and test equipment (emissions-related OBD). | Defines the Mode 01 reads this app uses. Text paywalled. | J1 |
| CARB 13 CCR 1968.2 | Notice lists SAE J1979, ISO 15765-4 (CAN, emission-related), SAE J1978 (scan tool) and SAE J2012 (DTC definitions) as incorporated documents; 2004 editions. | Confirms ISO 15765-4 CAN + J1979 as the legislated pipe. Current editions not verified. | R3 |
| 40 CFR 86.1808-01(f)(12) | For 2004 and later OBD vehicles with reprogramming capability, manufacturers "shall comply with SAE J2534" and must make pass-through reprogramming software available to aftermarket service providers; (f)(12)(v) bars requiring a manufacturer-specific scan tool for the hardware. (f)(17)(ii) requires J1979 compliance from MY2004. | J2534 governs pass-through reprogramming. A read-only ELM327 logger is not J2534 and does not reprogram. | R1 |
| SAE J2534-1 | A framework to allow reprogramming applications from vehicle manufacturers to work with tool-supplier interface hardware, for emission-related modules. | Not required for logging. Becomes relevant only if the app ever flashes. | J2 |
| 42 U.S.C. 7522(a)(3) (Clean Air Act s.203) | Prohibits removing or rendering inoperative any emissions device or element of design, and making, selling or installing a part whose principal effect is to bypass, defeat or render inoperative one. | A logger that only reads does neither. A feature that disables DTC logging (`$10 $02`) or clears DTCs and readiness would sit nearer this line. Another reason for the deny-list in 5.6. | R2 |
| Australia, Competition and Consumer Act 2010 Part IVE (MVIS) | Mandatory scheme for manufacturers to share service and repair information with Australian repairers and registered training organisations; applies to passenger and light goods vehicles made on or after 1 Jan 2002. Hobby repairers "cannot access service and repair information under this scheme"; manufacturers may still share with consumers. | Relevant to a Holden: a hobbyist gets no right to GM service data from the scheme. It does not restrict reading your own car's OBD port. | R4 |
| Right to repair, US state laws; ADR 79 OBD requirements for the VE | **Not retrieved: no primary source found.** | | |

Summary: nothing I read restricts an owner reading standard OBD data on their own vehicle. The legal edge lies in defeating emissions controls and in reprogramming, both outside a read-only logger.

---

## 9. Gaps and doubts

1. **SAE J1979 / ISO 15031-5 full text not read.** Formulas in section 2 come from C1 and C2; two spot-checks (0x0C, 0x05) are confirmed inside GM's G1. Range disagreements: 0x5C max (210 vs 215), 0x5E max (3212.75 vs 3277), 0x0E max (63.5 vs 64). The formulas themselves agree.
2. **SAE J2190 not read.** The history of Mode `$22` is unsourced here.
3. **ISO 15765-4 full text not read** (iso.org returned 403). Protocol facts come from E1 and G1.
4. **Which module is on 7E2 and 7E3 on a VE Series II: no primary source found.** G1 gives only slot numbers. "7E2 = TCM" and "7E0 = ECM" are conventional readings. "FPCM on 7E3" has no support.
5. **Whether the E38 supports PIDs 0x4F, 0x50, 0x43, 0x52, 0x5C, 0x5E:** no primary source found. Use the 0x00/0x20/0x40/0x60 bitmaps at run time.
6. **PFEFI-MAP2 datasheet: not found.** No Proflow/Holley transfer function. The "0.5-4.5 V over 20-270 kPa" assumption behind `62.5*V - 11.25` is unsourced. The "up to 1.9 bar" retail text conflicts with 2.7 bar absolute.
7. **Bosch 0 261 230 262 datasheet: not found.**
8. **GM 1/2/3-bar MAP transfer functions: no GM primary source found.** The 2-bar Delco calibration (0.30 V at 20 kPa, 4.80 V at 200 kPa) is a distributor drawing. The 3-bar figures are a seller snippet.
9. **151.3 kPa cap on stock E38 PID 0x0B: no primary source found.** Not explained by the one-byte (255) limit.
10. **E38 ADC resolution and reference voltage:** no primary source found. The `(A/255)` 8-bit form is the J1979 byte, not necessarily the ECU's ADC.
11. **E38 and T43 Mode 22 PID lists:** no primary source found. GM keeps these in CTS documents that are not public.
12. **GMW3110 read from a third-party mirror**, not GM. It is GM's text (text and page count match the cover: 336 pages, Feb 2010), but I cannot vouch for the copy. Which revision of GMW3110 the 2011 VE's E38 and T43 implement is unknown.
13. **6L80E documents:** GM's own clutch chart, solenoid layout and pressure-control current ranges were not retrievable. The chart in 6.3 is ATSG (secondary). The bulletin on adaptive learning (B2) is for the 8-speed.
14. **"T43 = 6L80/6L90 internal TCM":** supported by B1 plus H1 only by inference; the explicit statement is in forums.
15. **"1-8-9 clutch" for 6L80: no source supports it.**
16. **Pressure-control solenoid current range for the 6L80E: no primary source found.** Do not use the 4L60-E figure.
17. **FPCM: GMLAN message, ID, readable data and failure symptoms on a VE: no primary source found.** All FPCM text is from a 9-4X, a different vehicle.
18. **GM wiring/network documents for the VE** (module list, bus topology, DLC pins) were not found. DLC pins 6/14 are from a 9-4X page.
19. **J1979 Mode `$04` and `$08` meanings** used in 5.6 are general knowledge, not read from a primary text in this session.
20. **UDS (ISO 14229) service numbers** (`$2E`, `$14`, `$11`, `$31`, `$35`) are noted from general knowledge; ISO 14229 was not read. The GMW3110 statements about what is and is not in Table 6 are verified.
21. **CARB and 40 CFR references:** R3 lists 1997-2001 editions of the standards; current incorporated editions were not verified. The 86.1806-05(h) incorporation wording came only from search-result summaries and was not read first-hand.
22. **Right to repair (US state laws) and Australian ADR OBD requirements: not retrieved.**
23. **Retailer pages (M2) and a GM mode $06 PDF** were blocked or rate-limited on direct fetch; nothing from them is relied on.
24. **Wikipedia and forum content were used only as cross-checks, and every such use is tagged [S].**

Local scratch copies of fetched PDFs were kept in the session scratchpad only. No other file in the repo was modified.
