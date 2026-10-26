# BC Trans Calc_Shifts: grid semantics (from the decompile)

Source: `BC_Trans/BC_Trans/Main_Form.cs` (ILSpy 9.1 output) and `BCGrid/BCGrid/BCGridControl.cs`.
Line numbers refer to those files. The port is `app/tunertoolpro/bct/calc_shifts.py`.

## Grid storage

`BCGridControl` stores each table as a flat float array. `W_Data(x, y, v)` and
`R_Data(x, y)` use index `x + y * (Grid_X + 1)` (BCGridControl.cs:3975, 3986).

- x runs 1..Grid_X and y runs 1..Grid_Y. Index 0 is a header.
- Row y = 0 holds the TPS axis (x = 1..17). `Setup_Tables` writes `6.25 * (x - 1)`
  (Main_Form.cs ~5045, `U_Shift`, `D_Shift`, `Lock`, `Unlock`, `MinTCC`, `OverRide_Grid`).
- Column x = 0 holds the gear label (`U_Shift.W_Data(0, k, k + 1)` and similar).
- `W_Data` only writes when the control has `Init != 0` (BCGridControl.cs:3973).

`Calc_Shifts` and `Update_Slope` only run after `Init` has reached 2 (Timer1_Tick,
Main_Form.cs ~5909–5949). A grid write before that is dropped, so the port assumes
initialised grids.

## Dimensions (Setup_Tables, Main_Form.cs 4963–5100)

| Grid | X (TPS cols) | Y (rows) | Meaning of a row |
|---|---|---|---|
| `Ratio` | 1 | G | gear ratio |
| `RPM` | 1 | G | per-gear shift RPM (column 1) |
| `Speed` | 4 | G | per-gear speed columns, see below |
| `U_Shift` | 17 | G−1 | upshift speed from gear g to g+1 |
| `D_Shift` | 17 | G−1 | downshift speed from gear g+1 to g |
| `Lock` | 17 | G | TCC lock speed in gear g |
| `Unlock` | 17 | G | TCC unlock speed in gear g |
| `Slope` | 17 | 3 | 1 base, 2 upshift blend, 3 downshift blend |
| `Delay` (Lead_Form) | 2 | G−1 | column 1 Prep, column 2 React |
| `MinTCC` (TCC_Form) | 17 | 2G | col 2g−1 minimum TCC RPM for gear g; col 2g unlock-before-down flag |
| `OverRide_Grid` | 17 | 2(G−1) | manual slope; row 2n−1 upshift, row 2n downshift |

G is the gear count (`Gears`). The `MinTCC` columns are the file's
`MinTCCRPM<k>` / `MinTCCRPM<k>-<g>` and `TCC_UlckBeforeDown<k>` / `...-<g>` keys.

## Inputs read by Calc_Shifts

| Control | BTC key | Used for |
|---|---|---|
| `Gears` | `Gears` | G |
| `Ratio` col 1 | `Ratio1..G` | gear ratios |
| `Gear` ("Final") | `Gear` | final drive, multiplies every ratio |
| `Tire` | `Tire` | tire diameter (inches) |
| `Idle` | `Idle` | MinSpeed uses Idle + 400 |
| `DRPM` | `DownRPM` | downshift speed cap |
| `Stall` | `Stall` | stall slip, and StallMin |
| `RPM` col 1 | `RPM1..G` | shift RPM per gear (clamped at the top of Calc, lines 5218–5232) |
| `Lead_Form.Weight`, `RWHP` | `Weight`, `RWHP` | torque-based lead acceleration |
| `Lead_Form.Lead` | `Lead` | RPM-based lead value |
| `Lead_Form.Lead_Radio1` | `AdvancedLead` (0 = RPM lead) | selects RPM or torque lead |
| `Lead_Form.Down_Time` | `DownTime` | torque lead downshift time |
| `Lead_Form.TCC_Delay` | `TCC_Delay` | WOT lock delay |
| `Lead_Form.Delay` | `Prep1..G-1`, `React1..G-1` | per-shift delay pairs |
| `Factor`, `Offset`, `UpF`, `DownF` | `Factor`, `Offset`, `UpFactor`, `DownFactor` | Update_Slope |
| `Shift_Spread` | `ShiftSpread` | upshift spacing and downshift spacing |
| `Lock_Spread` | `LockSpread` | Lock = Unlock + LockSpread |
| `Lock_Shift_Spread` | `ShiftLockSpread` | accelerator-lock spacing |
| `Unlock_Shift_Spread` | `UnlockShiftSpread` | Unlock = D_Shift + this |
| `MinLck` | `MinLockGear` | gears below this get disabled lock cells |
| `AclLck` | `AccelLockGear` | accelerator-lock gear, used by the lock passes |
| `WotLck` | `WOTLockGear` | WOT lock gear |
| `WOTLockRPM` | `WOTLockRPM` | WOT lock RPM (changed by AUTOWOT) |
| `CheckBox1` (AUTOWOT) | `AUTOWOT` | sets WOTLockRPM and WOTStayLocked |
| `WOTStayLocked` | `WOTStayLocked` | WOT lock stays at the upshift − 1 |
| `StallLogic` | `StallLogic` | stall-based lock floor |
| `InitLock` | `AccelGearLock` | accelerator-lock pass |
| `PreLock` | `PreAccelGearLock` | pre-lock pass |
| `PostLock` | `PostAccelGearLock` | post-lock pass |
| `ULckStay` | `UnlockStay` | keeps unlock before the next downshift |
| `LockUnlock` | `Lock>Unlock` | Lock ≥ Unlock + LockSpread |
| `UpDown` | `Up>Down` | upshift ≥ downshift + ShiftSpread |
| `ShiftMax` | `Shift<Max` | clamps U and D to Speed columns 3 and 4 |
| `MaxSpeed_Locked` | `UseLockedSpeed` | selects Speed col 1 or 2 for lead |
| `WOTTCCPrep` | `WOTTCCPrep` | extra lock/unlock cells at WotLck − 1 (needs Trans ≥ 3) |
| `ComboBox1` | `Trans` | transmission preset index (rules at 1 and ≥ 3) |
| `Allow4L60WOT4th` | `Allow4L60WOT4th` | disables U row 3 columns 13–17 when off and Trans = 1 |
| `No2CT_6L` | `No6L_CT2nd` | copies D row 1 to row 2 columns 1–3 (Trans ≥ 3) |
| `DynoMode` | `DynoMode` | copies column 1 across the row for D, Lock, Unlock |
| `RRM` | `RollRaceMode` | copies the edge column across the row for U, D, Lock, Unlock |
| `SGS` | `SecondGearStart` | zeroes U and D row 1 |
| `OverRide_Enable` | `SlopeOverride` | uses the manual slope grid instead of Slope |
| `Metric` | `Metric` | display scale only (KPH factor 1.609), not used in the math |

Not read by Calc_Shifts: `TCC_MinRpm`, `TCC_MinTps`, `TCC_MaxTps`, `MinTCCRPM` as a
scalar (only the grid), `VSS`, `TBSlope`, the `Exp_*` keys, `LeadShiftRPM`.

## Speed grid (Calc_Shifts, 5258–5330)

Column 1, shift speed at RPM: `speed(RPM_g, Ratio_g, Gear)`.
Column 2: `Speed1 * (1 − stall_slip)`, where `stall_slip = (Stall/1000)^1.7 / 100`.

Column 3 (lead), and column 4 (downshift):

- RPM lead (`AdvancedLead == 0`):
  `S3 = base*(1 − 0.01·R·F·L/8) − (R+1)·F·L/8`, floored at 0.2·S2.
  `S4 = S3·0.98 − 2 − R·F·(1 + L/10)·0.5`, capped at the DRPM speed and floored at 0.2·S3.
  This branch has no Shift_Spread cap and uses `continue`.
- Torque lead (`AdvancedLead == 1`): `accel = RWHP·0.75·375/base/Weight·21.93685`.
  `S3 = base − accel·(Prep+React)`, `S4 = base − accel·(DownTime+Prep+React)`.
  Delay row is `min(g, G−1)`, so the top gear uses the last shift's pair.
  Then S4 is capped at DRPM, capped at `S3 − ShiftSpread`, and floored at 0.2·S3.

`base` is Speed col 2, or col 1 when UseLockedSpeed is on and g ≥ WotLck.

## Upshift and downshift (5331–5360)

`MinSpeed[n] = speed(Idle + 400, Ratio_n, Gear)`.
`U(c, n) = MinSpeed[n] + S + ((Speed1[n] − MinSpeed[n]) − S) · slopeU(c)`, with S = ShiftSpread.
`D(c, n) = MinSpeed[n] + (Speed4[n] − MinSpeed[n]) · slopeD(c)`.
`slopeU` is `Slope(c,2)`, and `slopeD` is `Slope(c,3)`. With SlopeOverride on they come from
`OverRide_Grid(c, 2n−1)` and `OverRide_Grid(c, 2n)`.

## Slope (Update_Slope, Main_Form.cs 5113–5212)

`x = clamp(TPS_c − Offset, 0, 100) / 100`, with `TPS_c = 6.25·(c−1)`.

- Base: `Slope(c,1) = x^Factor`, clamped to [0,1]. Forced: `(1,1)=0`, `(17,1)=1`.
- Upshift: `y = 1 − (1−x)^(Factor + UpF/10)`. Blended with the base slope by a 17-entry
  table (`SLOPE_BLEND`, the same as CalcEngine). Forced: `(1,2)=0`, `(17,2)=1`.
- Downshift: `Slope(c,3) = x^(Factor + 0.1 + (10 − DownF)/5)`. Forced: `(1,3)=0`, `(17,3)=1`.

## Lock and unlock (5361–5410, then the do-while loop)

- MinTCCSpeed: `MinTCC(k, 2g−1)` converted to MPH with Ratio_g and Gear.
- Unlock row 1 is zeroed. Row g ≥ 2 is `D(c, g−1) + UnlockShiftSpread`. Every cell is floored at MinTCCSpeed.
- Lock = Unlock + LockSpread for every cell.
- StallLogic: each Lock cell is floored at a stall-based speed. Note the off-by-one:
  the code reads `StallMin[c − 1]` (5381), but `StallMin[l]` is only set for l = 1..17 (5263).
  So column 1 reads a null entry (0), and column c reads the value computed for c − 1.
  The port keeps this.

## Iteration (do-while, 5388–5606)

Up to 32 passes. Each pass runs, in order:
InitLock, PreLock, PostLock, Unlock→D, ULckStay, LockUnlock, UpDown, ShiftMax.
It stops when a pass changes nothing. `num` is only used for the "logic error" label.
The `SData` selection bits are display-only (`Clear_Selected`, BCGridControl.cs:5932).

## Post-loop steps (5607–5920)

1. Lock = Unlock where `MinTCC(c, 2g) == 2`.
2. AUTOWOT: set WOTLockRPM = 1000 and WOTStayLocked = off.
3. WOT lock for each gear g from WotLck up. For columns 15–17:
   - AUTOWOT: if WOTLockRPM is 1000, set it to `floor(RPM_g·0.8/50)·50` (persists for later gears).
     If g > WotLck and Lock − U(17, g−1) < 15, set WOTStayLocked on.
   - `Lock = Speed1·(WOTLockRPM/RPM_g) − accel·TCC_Delay`.
   - If g > WotLck and WOTStayLocked: `Lock = U(17, g−1) − 1`.
   - `Unlock = Lock·0.95 − 1`.
4. Monotone pass on Lock and on Unlock: cell c−1 is floored to cell c, from c = 17 down to 2.
5. Disabled cells: Lock < MinLck (columns 1–14) and Lock < WotLck (columns 15–17) are
   set to the markers. Lock = 255 and Unlock = 254 when Gears ≤ 4, otherwise 318 and 317
   (Dis_High / Dis_Low, Main_Form.cs ~4550).
6. WOTTCCPrep: if on, WotLck in [2, G+1], and Trans ≥ 3, set cells at WotLck − 1 in columns
   15–17 to `U(17, a) + 2` (Lock) and `+ 1` (Unlock).
7. Allow4L60WOT4th: when off and Trans = 1, U row 3 columns 13–17 = disabled.
8. No2CT_6L: when on and Trans ≥ 3, D row 2 columns 1–3 copy row 1.
9. DynoMode: copy column 1 across D, Lock and Unlock.
10. RRM: copy column 17 to columns 1–16 for U and D, and column 1 to 2–17 for Lock and Unlock.
11. SGS: zero U and D row 1.
12. Clamp every negative U, D, Lock and Unlock cell to 0.
13. Export_Form updates (display only, not ported).

## What the BTC file does not store

- The `U_Shift`, `D_Shift`, `Lock`, `Unlock`, `Speed` and `Slope` grids are not in the tune.
  They are recomputed from the keys above.
- `WOTTCCPrep` is set to on by `Read_Trans` (6644) when the key is absent. The shipped
  tunes all store it.
- `OverRide_Enable` is off in all 33 shipped tunes (`SlopeOverride` = 0).
- `SData` selection bits are not stored.

## Float precision

BC stores grid values as 32-bit floats. The port rounds each store to float32.
Intermediate arithmetic is done in double, as the decompile does for most expressions.
A small last-digit difference from BC is possible.

Comparisons follow the same rule. BC casts the sum to `float` before comparing it with a
stored cell (for example `num3 = (float)(... + Val(spread))`, then `if (cell < num3)`).
The port rounds the operand the same way. A first version did not, and five 4-gear
tunes never settled, because a sum that rounded down was never reached by the stored cell.
This is now fixed. All 33 shipped tunes converge in 2 or 3 passes, with no logic error.

## Port status

- `app/tunertoolpro/bct/calc_shifts.py` ports Update_Slope, Calc_Shifts and the option steps.
- Tests: `app/tests/test_calc_shifts.py` (11 tests). They check a hand-worked speed,
  the stall column, convergence on all 33 tunes, grid shapes, the disabled markers, the
  AUTOWOT WOT lock, the override grid, and missing-key errors.
- Differentially checked against the decompiled `Calc_Shifts` (verbatim copy of
  Main_Form.cs 5113-5897, run under .NET 8 with WinForms controls stubbed). 433 cases:
  the 33 shipped tunes plus 400 seeded random variants. Every U, D, L, N, S and P cell
  agrees within 5.0e-05. The logic-error flag agrees on all cases. Bit-identical float32
  values account for 47,367 of 182,445 cells. The rest differ by a few float32 ulps from
  operation order. Run with your approval on 2026-10-27, in an empty folder, `python3 -I`,
  no network. This is not a check against BC Trans itself, which cannot be run here.
- The Shift Points tab still uses `CalcEngine`. Its inputs come from
  `bct/shift_cfg.py`, which is not the same algorithm as this port.

Differences from `CalcEngine` that matter for the mapping:

- BC Trans's `Calc_Shifts` reads the per-cell `MinTCC` grid. It does not read the
  scalar `TCC_MinRpm`, which `shift_cfg.py` maps to `min_tcc_rpm`. That key is a
  substitute, and BC Trans does not use it.
- The `Lead`, `Speed` and delay formulas follow BC Trans, not CalcEngine's
  transcription.

## Verification

- Differential run (approved): see the first bullet under "Port status" above. The only
  mismatch found during the work was a harness bug: a BTC value with a leading space
  (`LockSpread` ` 2` in the 8L90 tunes) was written as a double-spaced case line and read
  as empty, so the oracle used 0. The port was right; the generator now strips values.
- Still open: a check against BC Trans output on a real car or a live run of BC Trans.
