"""The T43 transmission PIDs from the confirmed list (26_LATEST_TorquePro_PIDs_E38_T43_v5.csv).

pid_table.py is generated from the VE CALAIS Kotlin source and must not be edited by hand, so the corrections
live here and pids.py puts them over the generated rows. The generic rows they replace were marked "probable"
in the generated table and were never confirmed on the T43. Every row here reads the transmission module at
header 7E2, the address the T43 list uses.

Two decisions are the user's to check on the car:
- 221941 (input shaft speed): the list has two formulas for this PID. Here it is ((A*256)+B)/4. The "div8" row,
  ((A*256)+B)*0.125, is the other candidate. The gear-follow check in live.py depends on this choice.
- 22194F was the generic fluid-temperature guess. The confirmed PID is 221940, and 22194F is removed.
"""

# (pid, name, category, unit, low, high, description, header, kind, decode) - the same shape as pid_table.ROWS.
ROWS = [
    ('221940', 'Trans Fluid Temp (T43)', 'Transmission (T43)', '°C', -40.0, 150.0,
     'T43 transmission fluid temperature, from the confirmed T43 list (A-40, module 7E2)',
     '7E2', 'byte', lambda x: x - 40),
    ('221991', 'TCC Slip (T43)', 'Transmission (T43)', 'rpm', -1000.0, 4000.0,
     'T43 torque converter clutch slip, signed, from the confirmed T43 list (module 7E2)',
     '7E2', 'word', lambda x: (x - 65536 if x >= 32768 else x) / 8.0),
    ('221992', 'Last Shift Time (T43)', 'Transmission (T43)', 'sec', 0.0, 6.0,
     'T43 duration of the last shift, from the confirmed T43 list (A/40, module 7E2)',
     '7E2', 'byte', lambda x: x / 40.0),
    ('221941', 'Input Shaft Speed (T43)', 'Transmission (T43)', 'rpm', 0.0, 8000.0,
     'T43 input shaft speed, from the confirmed T43 list ((A*256)+B)/4, module 7E2',
     '7E2', 'word', lambda x: x / 4.0),
    ('221942', 'Output Shaft Speed (T43)', 'Transmission (T43)', 'rpm', 0.0, 8000.0,
     'T43 output shaft speed, from the confirmed T43 list ((A*256)+B)*0.125, module 7E2',
     '7E2', 'word', lambda x: x * 0.125),
    ('22199A', 'Current Gear (T43)', 'Transmission (T43)', 'gear', 0.0, 6.0,
     'T43 current gear, from the confirmed T43 list (A, module 7E2)',
     '7E2', 'byte', lambda x: x),
]

# Generic rows dropped entirely, because they name a PID the confirmed list does not have.
REMOVED = ('22194F',)
