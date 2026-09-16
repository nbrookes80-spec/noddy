# VE Calais OBD2 Scanner - Troubleshooting & Setup Guide

## Problem: App Not Reading PID Data

The app wasn't reading PIDs because of **critical ELM327 communication issues**:

### Root Causes Fixed

1. **Response Reader Was Incomplete**
   - ELM327 with `AT H1` (headers on) returns: `[HEADER] [DATA] [>]`
   - Old code only read ONE line, causing it to miss the actual data
   - **FIXED**: Now reads all lines until prompt `>` is found

2. **OBD2 Command Formatting Was Wrong**
   - Mode 01 PIDs need format: `01XX` (e.g., `010C` for RPM)
   - Mode 22 PIDs need format: `22XXXX` (e.g., `221991` for TCC Slip)
   - Response parsing was skipping the mode echo incorrectly
   - **FIXED**: Proper command formatting and response parsing

3. **Header Switching Not Validated**
   - `AT SH` commands weren't waiting for confirmation
   - Caused mode switching to fail silently
   - **FIXED**: Synchronized header changes with response verification

4. **Blocking I/O on Coroutines**
   - `Thread.sleep()` in async context freezes UI
   - **FIXED**: Replaced with proper coroutine delays

---

## What Changed

### Updated Files
- **BluetoothManager.kt**: Fixed ELM327 response reading (multi-line, until prompt)
- **OBD2Protocol.kt**: Proper command formatting and response extraction
- **CustomPIDManager.kt** (NEW): Add/import/export custom PIDs
- **CustomPIDFragment.kt** (NEW): UI for managing custom PIDs
- **fragment_custom_pid.xml** (NEW): Layout for custom PID manager

### Current PID Database
The app already includes:
- **40+ Mode 01 SAE Standard PIDs** (universal OBD2)
- **60+ Mode 22 GM Enhanced DIDs** (E38 ECU & 6L80E TCM specific)
- **Per-cylinder data**: Misfire counts, injector pulse width, fuel balance (L77 V8)
- All previously problematic PIDs are now correctly formatted

---

## How to Test (Demo Mode First)

### Step 1: Test Without Car (Demo Mode)
1. Open the app → **Home** tab
2. Toggle **Demo Mode** ON
3. Go to **Live Data**
4. Tap **Start Monitoring**
5. You should see simulated data changing every 500ms
6. Tap any sensor card to cycle: Digital → Graph → Histogram

**Expected**: Values show in all 3 display modes, data updates smoothly.

---

## How to Connect to Your Car

### Prerequisites
1. **Bluetooth adapter** (ELM327 compatible) - must support CAN, 500kbaud
2. **2011 VE Calais paired via Bluetooth** (Settings → Paired Devices)
3. **Car running** (to provide power to OBD2 port and respond to queries)

### Connection Steps
1. **Home** tab → Tap **"Connect to OBD2 Adapter"**
2. Select your ELM327 adapter from the list
3. Wait for "Connected" status (green indicator)
4. Go to **Live Data** → Tap **Start Monitoring**
5. Watch for real sensor values

### What Should Happen
- First few requests may timeout (adapter initialization)
- By request #3-5, you should see real ECU data
- Temperatures, RPM, throttle, etc. should match car state
- Data updates every 500ms

---

## Troubleshooting Checklist

### Problem: "Connected but no data"

**Try this sequence:**

1. **Check adapter compatibility**
   ```
   Open Sniffer → look for responses to AT commands
   Should see: OK, >
   If you see nothing → adapter not responding
   ```

2. **Verify CAN protocol** (Sniffer tab)
   - Send: `AT SP6` (protocol for CAN 11-bit)
   - Expected: `OK` or `?` if unsupported
   - If `?` → your adapter doesn't support CAN
   - Try `AT SP4` (KWP2000) but it won't work for E38

3. **Test basic Mode 01 PID** (Sniffer)
   - Send: `010C` (RPM, should work on any OBD2)
   - Expected: `41 0C XX XX` (with real data)
   - If "NO DATA" → ECU not answering at all
   - If nothing → adapter is silent

4. **Test GM Mode 22** (Sniffer, after confirming Mode 01 works)
   - Send: `AT SH 7E0` (switch to ECM)
   - Send: `221991` (TCC slip - 6L80E TCM)
   - Expected: `62 19 91 XX XX` (if TCM is on 7E2, this will fail)
   - Try: `AT SH 7E2` then `221991` again

### Problem: "Some PIDs timeout, others don't"

**This is normal** — your E38 may not support every PID in the database. The database is compiled from multiple sources and includes some unverified PIDs.

**What to do:**
1. Open **Settings** → Uncheck PIDs that timeout (remove them from monitoring)
2. Keep the ones that respond:
   - Core PIDs always work: RPM (010C), Coolant (0105), Throttle (0111), Speed (010D)
   - Your car may not support: Oil temp, Barometric pressure, some O2 readings
3. Use **Custom PID Manager** to add PIDs you know work (from Torque Pro, etc.)

### Problem: "Temperatures reading wrong (frozen, negative, etc.)"

**Cause**: Parsing formula mismatch.

**Fix**: Check the parsing formula in **Settings** (read PID descriptions):
- Coolant: should be `-40°C` at startup, rise to ~85°C when warm
- If frozen at wrong temp → formula is wrong
- Custom add the PID with correct formula (see below)

### Problem: "Transmission data not showing"

**Check header routing:**
1. **Sniffer** tab
2. Send: `AT SH 7E2` (TCM header for T43)
3. Send: `221991` (TCC slip)
4. If you get `62 19 91 XX XX` → PID works, header is correct
5. If "NO DATA" → TCM doesn't answer on 7E2
   - Try: `AT SH 7E1` (old/alternate TCM address)
   - Try: `AT SH 7DF` (broadcast - might get echo)

---

## Adding Custom PIDs

### When to Use
- Found a PID in Torque Pro that works but isn't in our database
- Your car responds to a PID we list as "unverified"
- Want to add a tuner-specific DID from your tune file

### Steps

#### Option A: Manual Entry
1. **Custom PID Manager** screen (new tab in settings)
2. Fill in:
   - **PID Code**: `221991` (hex, 4-6 digits)
   - **Name**: "TCC Slip Speed"
   - **Category**: "Transmission"
   - **Unit**: "RPM"
   - **Min/Max**: `0` / `10000`
   - **Description**: "Torque converter slip"
   - **Header**: `7E2` (TCM address, or `Auto` for Mode 01)
   - **Formula**: `(A*256)+B` (parsing rule)
3. Tap **Add Custom PID**

#### Option B: CSV Import
1. Create a CSV file with your PIDs:
   ```
   PID,Name,Category,Unit,Min,Max,Description,Header,Formula
   221991,TCC Slip,Transmission,RPM,0,10000,Torque converter slip,7E2,(A*256)+B
   22001F,Trans Pressure,Transmission,kPa,0,3000,Line pressure,7E2,(A*256)+B
   ```
2. **Custom PID Manager** → **Import CSV**
3. Navigate to the file and select

### Formula Reference

| Formula | Example | Meaning |
|---------|---------|---------|
| `A` | Engine Load | Single byte, direct value |
| `A-40` | Coolant Temp | Single byte, subtract 40 |
| `A*0.5` | Boost | Single byte, multiply by 0.5 |
| `A/2.55` | Percentage | Single byte, scale to 100% |
| `(A*256)+B` | RPM, Pressure | Two bytes, 16-bit value |
| `(A-128)` | Spark Advance | Signed byte (-128 to +127) |

### Header Reference

| Header | Module | Use For |
|--------|--------|---------|
| `Auto` | Functional (Default) | Mode 01 PIDs (standard SAE) |
| `7E0` | ECM (Engine) | Mode 22 engine PIDs |
| `7E2` | TCM (Transmission) | Mode 22 transmission PIDs |
| `7E3` | FPCM (Fuel Pump) | Mode 22 fuel pump PIDs (unconfirmed) |

---

## Example: Adding a Verified PID

**Scenario**: You have Torque Pro, you found PID `221950` responds on your car with trans fluid temp.

**How to add:**
1. Note the response format from Torque: `62 19 50 XX`
2. Determine the formula:
   - If single byte: `A-40` (typical for temp)
   - If matches our existing trans temp formula: copy that
3. Open **Custom PID Manager**:
   - PID Code: `221950`
   - Name: `Trans Fluid Temp Alt`
   - Category: `Transmission`
   - Unit: `°C`
   - Min: `-40` , Max: `200`
   - Header: `7E2`
   - Formula: `A-40`
4. Tap **Add Custom PID**
5. Go to **Settings** → Check the new PID
6. **Live Data** should now show the value

---

## Data Logging

### Auto-logging (Every Session)
- Every time you tap **Start Monitoring** → new session begins
- Logs are **auto-saved** when monitoring stops (date-stamped)
- Files: `session_2026-09-16_143052.csv` & `.json`
- Location: `/storage/emulated/0/Android/data/com.brookes.ve_calais_obd2/logs/`

### Export Mid-Session
1. **Live Data** → **CSV** or **JSON** buttons
2. Exports current session on demand
3. Useful if you want a snapshot before drive

---

## Suggestions for Easier Setup

### 1. **Use Demo Mode for Testing**
- Test all features without the car
- Verify UI is working before connecting
- Saves Bluetooth pairing/connection troubleshooting

### 2. **Start with Core PIDs Only**
- Don't monitor all 100+ PIDs at once
- Start with: RPM, Coolant, Intake Temp, Throttle, Speed
- Add more once core PIDs are confirmed working

### 3. **Use Sniffer Tab for Diagnostics**
- Before giving up on a PID, test it in Sniffer
- Send the raw command and see the response
- Helps identify bad header, bad formula, or missing PID

### 4. **Save Working PID Lists**
- Once you confirm a PID works, screenshot the Sniffer response
- Export custom PIDs as CSV backup
- Share with other VE Calais owners

### 5. **Check Torque Pro for Reference**
- If you already have Torque, check which PIDs respond
- Copy the PID code and formula to our app
- Our database inherits from Torque exports but may have gaps

### 6. **Join VE Calais OBD2 Community**
- Share your working PID list on forums
- eg. PCMhacking, EFILive forums, LS1TECH
- Help others fill in blanks for E38/6L80E/T43

---

## Next Steps

1. **Compile the updated app** (Android Studio)
   - Sync Gradle
   - Rebuild project
   - APK will be generated

2. **Install on your phone**
   - Transfer APK or use Android Studio "Run"
   - Grant Bluetooth permissions when prompted

3. **Test with Demo Mode first**
   - Verify all screens work
   - Test data export
   - Confirm display modes cycle

4. **Connect to your car**
   - Follow connection steps above
   - Use Sniffer for diagnostics
   - Add custom PIDs as needed

5. **Log your data**
   - Run monitoring for a drive
   - Export CSV/JSON
   - Share results (or keep for personal diagnostics)

---

## Reference: Full PID List

See **PIDDatabase.kt** for the complete list (140+ PIDs). Key categories:

- **Engine**: RPM, Coolant, Intake Air Temp, Load, Timing, Oil Temp
- **Turbo**: MAP (3-bar scaled), Barometric Pressure
- **Fuel**: Rail Pressure, Trim, O2 Sensors, Ethanol %, Injector PWM
- **Transmission** (GM Mode 22): Current Gear, TCC Slip, Fluid Temp, Line Pressure, Shift Times, Input/Output Speed, Solenoid Current
- **Electrical**: Ignition Voltage, Battery Voltage
- **Per-Cylinder**: Misfire Counts, Injector Pulse Width, Fuel Balance

All are documented with:
- Correct CAN header (7E0 for ECM, 7E2 for TCM)
- Parsing formula (how to convert raw bytes to real value)
- Min/Max range for this specific hardware
- Status: "Verified" (confirmed on this VIN) vs. "Probable" (from database, not yet confirmed)

---

## Contact & Support

Issues or questions?
1. Check Sniffer output (diagnostic step)
2. Share Sniffer response + full error message
3. File issue on the GitHub repo (when available)

**This app is purpose-built for your 2011 VE Calais L77/E38/6L80E/T43 setup. Hardware accuracy is non-negotiable.**
