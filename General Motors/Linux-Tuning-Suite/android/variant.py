"""What this build is: its name, its version, and which features it was built with. No Kivy.

V2.10 is a separate build with its own Android package, so the 0.4.0 app stays installed beside it with its own
settings. CLEAR_CODES is the one switch that changes what the car is asked to do: 0.4.0 was read-only, V2.10 may
clear stored trouble codes (Mode 04), behind a confirmation on the Scan tab. Rebuilding 0.4.0 from this tree needs
CLEAR_CODES set back to False.
"""

NAME = 'TunerToolPro V2.10'
VERSION = '2.10'
CLEAR_CODES = True
