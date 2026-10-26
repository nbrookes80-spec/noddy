# Working with EFILive and HP Tuners

This guide covers how TunerToolPro works with the files from EFILive and HP Tuners, what is
built, what is not, and the steps you take yourself.

## Summary

- **Reading EFILive calibration exports: built.** `app/tunertoolpro/efilive_export.py` reads the
  text export that EFILive Tune writes and turns it into a readable summary. The AI uses that
  summary when you import an export in the Vehicle tab.
- **Writing to a vehicle: not built, on purpose.** TunerToolPro never sends a calibration to a
  controller. The AI can prepare and propose changes, but you make each change yourself in
  EFILive or HP Tuners, then write it to the car. See "Why the AI does not write to the car" below.
- **HP Tuners files: not yet decoded.** The `.HPT` file in your Downloads folder is an EFILive
  export, not an HP Tuners file (see Findings below).

## Manual workflow (no AI needed)

1. In EFILive Tune, export the calibration. The export dialog offers "Comma delimited text
   files (*.csv)".
2. In TunerToolPro, open the **Vehicle** tab and click **Import EFILive export...**. Choose the
   file. The tab shows how many values and tables were read.
3. Fill in the vehicle details and ECU limits, then click **Save vehicle**. Save copies the
   tire, final drive and weight into the **Shift Points** tab, where the calculation uses them.
4. Use **Check consistency** on the Vehicle tab. Read each finding before you change anything.
5. Calculate on the **Shift Points** tab and compare with the export.
6. Make any change in EFILive Tune yourself, then write it to the controller with EFILive.

You can also print the summary from a script, without the app:

```
python3 -I -m tunertoolpro.efilive_export "/path/to/export.csv"
```

Run it from the `app` folder, and keep the export in its own folder. The `-I` flag stops Python
from loading modules from the current folder.

## AI workflow (optional)

1. Turn on the AI Assistant and save your API key (AI Assistant tab).
2. Import the export on the Vehicle tab. The AI reads the export summary with the other settings.
3. Ask a question. Any change the AI suggests appears in the **Proposed changes** table with
   **Apply** and **Reject**. Nothing changes until you press Apply, and Apply only changes the
   numbers inside TunerToolPro, within their allowed ranges.
4. If you apply a change, make the same change in EFILive or HP Tuners yourself and write it to
   the car.
5. If the AI needs a value it cannot find (for example, the number of gears or the converter
   stall rating), it asks you in the answer. Reply in the question box and press Ask again.

## Why the AI does not write to the car

The AI could be given a tool to send a calibration to EFILive or HP Tuners and write it to the
controller. Three reasons it is not:

- A bad write to a transmission or engine controller can damage the car or make it unsafe, and
  it may not be undone by a second write if the tool stops partway.
- The AI's suggestions are not checked by TunerToolPro against the controller's own limits. Only
  you can judge the result on the road or on the dyno.
- Changes that affect torque limits or emissions controls may be illegal to make for road use in
  some places, and that is your decision to make.

So the boundary is: the AI prepares and explains, the app checks and records, and you write.

## Findings from the sample files

These come from static reading of your files and the installed EFILive V7.5 program. EFILive was
not run.

- **The `.HPT` file is a text export from EFILive.** It starts with `"EFILive Calibration Export"`
  and is CRLF text. The extension says HP Tuners, but the contents are EFILive's.
- **The `.HPT` and the CSV in your Downloads are two saves of the same tune.** They have the same
  layout. Their export times are 01:42:33 and 03:29:36 on 15 Aug 2026. 27 of the records differ
  between them, so the tune was changed between the two saves.
- **Record layout.** Each line starts with a code: `D` for calibration values and tables, `E` for
  enable flags, `P` and `U` for trouble codes, `H` for vehicle constants. Scalars are
  `CODE,value,unit,"label"`. Tables have a title, then header and data rows. The reader is in
  `app/tunertoolpro/efilive_export.py`, with tests in `app/tests/test_efilive_export.py`.
- **Vehicle constants in your tune** include an axle ratio of 3.910034, a tire size correction of
  1.000001, and 36 speed sensor pulses per revolution. Check these against your car. A wrong
  axle ratio makes every speed-based shift point wrong.
- **The `.calz` files in the EFILive install** (`V7.5/Calibrations/T43/`) have no readable header
  and look encrypted from the first byte. They are not decoded, and I have not tried to break
  their protection. Plain-text exports are the supported route.
- **EFILive log files** are named in the program's messages (for example "is not a valid EFILive
  log file"). Their layout is not yet worked out.

## HP Tuners

There is a Windows VirtualBox machine named "WINDOWS HP TUNERS" on this computer. Its disk image
has not been examined. Reading it would mean mounting the disk image, which needs your approval
first. Until then, the way to get HP Tuners data into the app is an export from HP Tuners to a
text or CSV file, handled the same way as the EFILive export.

## Next steps (you choose)

1. Export a calibration from HP Tuners as CSV or text, and send it so the reader can be checked
   against it.
2. Approve examining the HP Tuners disk image, to see whether its file format can be read.
3. Decide on EFILive log files: send a log export, and the log reader can be built against it.
