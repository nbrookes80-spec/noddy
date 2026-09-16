# VE Calais L77 OBD2 Reader - Quick Start Guide

**For:** Nathan Brookes (FOX95S)  
**Vehicle:** 2011 Holden VE Calais Redline L77  
**Get Started In:** 5 minutes

---

## 30-Second Summary

This Android app connects to your OBD2 ELM adapter via Bluetooth and displays **live engine, fuel, boost, and transmission data** from your E38 ECU in real-time. It logs all data to CSV/JSON for analysis and is **locked to your vehicle** via VIN/ECU verification.

**Install** → **Pair Adapter** → **Start Monitoring** → **Export Data**

---

## Installation Quick Start

### 1. Install the App (2 minutes)

**Option A: Android Studio (Recommended)**
```bash
# Extract files
cd VE_Calais_OBD2

# Open in Android Studio
# Build > Build APK(s)
# Run > Run 'app'
```

**Option B: Direct APK**
- Download `app-debug.apk`
- Transfer to Android phone
- Tap to install
- Grant permissions

### 2. Pair OBD2 Adapter (1 minute)

On your phone:
1. Settings > Bluetooth
2. Turn ON
3. Put adapter in pairing mode
4. Tap adapter name to connect
5. PIN: `0000` or `1234` (check adapter manual)

### 3. Launch App (30 seconds)

1. Tap app icon
2. Select Bluetooth adapter
3. Go to "Live Data" tab
4. Start your car engine
5. Tap **"Start Monitoring"**

**That's it!** Live data appears instantly.

---

## What You're Seeing

### Main Dashboard

**Top Row - Engine Status:**
- RPM, Coolant Temp, Boost (MAP), Engine Load
- Updates every 500ms

**Second Row - Fuel System:**
- Fuel Pressure, O2 Sensors, Fuel Trim
- Critical for tuning feedback

**Third Row - Transmission:**
- Current Gear, Trans Temp, Shift Pressure, TCC Slip
- 6L80E-specific monitoring

### Color Coding

🟢 **Green** = Normal operating range  
🟡 **Yellow** = Caution (monitor closely)  
🔴 **Red** = Critical (stop driving)

---

## Data You Can Monitor

### Real-Time Engine Parameters (12+)
- **RPM** (0-8000)
- **Coolant Temperature** (-40 to 125°C)
- **Boost Pressure** (0-270 kPa) - 2.7 Bar sensor
- **Engine Load** (0-100%)
- **Fuel Pressure** (0-765 kPa)
- **Ignition Timing** (-64 to +64° BTDC)
- **Intake Air Temperature** (-40 to 215°C)
- **Vehicle Speed** (0-300 km/h)

### Turbo-Specific Monitoring
- MAP sensor reading (confirms 2.7 Bar sensor)
- Boost pressure trending
- Intake temp under boost
- Fuel pressure vs boost correlation

### Transmission (6L80E)
- Current gear (P, R, N, D, 3, 2, 1)
- Transmission fluid temp (critical for boost runs)
- Shift pressure (Transgo kit verification)
- TCC lockup speed (confirms hard lockup tuning)

### Fuel System
- Fuel pressure stability (500 kPa base)
- O2 sensor voltages (tuning feedback)
- Short/long term fuel trim (E85 flex tune)

---

## Export Your Data

### After Each Session

1. **Tap "Stop Monitoring"**
2. Choose export format:
   - **CSV** - For Excel or EFI Live
   - **JSON** - For analysis tools
   - **PDF Report** - Statistical summary

3. Files save to: `Phone/Documents/VECalaisLogs/`

### Use Cases

**EFI Live Analysis**
- Export as CSV
- Open in EFI Live datalog viewer
- Overlay with tune parameters

**Dyno Comparison**
- Export before/after tuning
- Compare fuel trim, boost curve, timing
- Track performance improvements

**Troubleshooting**
- Export when issue occurs
- Share with tuner for analysis
- Diagnose fueling or trans issues

**Data Logging**
- Export daily for trend analysis
- Monitor component health
- Alert on abnormal readings

---

## What Each Parameter Means

### Engine Management

**RPM** - Engine speed. Normal idle: 600-900 RPM.

**Coolant Temp** - Engine heat. Normal: 85-95°C. Above 100°C = getting hot.

**Boost (MAP)** - Turbo pressure. 
- Idle: ~100 kPa (atmospheric)
- Cruise: ~120 kPa
- WOT: 200-270 kPa (hard on boost)

**Engine Load** - How hard the engine is working.
- 0-20% = Cruising
- 20-50% = Normal driving
- 50-80% = Hard acceleration
- 80-100% = Full throttle

**Fuel Pressure** - Rail pressure from KPM pump.
- Should be stable ~450-500 kPa
- Drops under high load if pump failing
- Rising with boost = working correctly

**Ignition Timing** - Spark advance.
- Idle: 20-30° BTDC
- WOT turbo: 10-15° BTDC (more conservative than NA)
- Negative values = retard for safety

**Intake Air Temp** - Turbo charge air temperature.
- Normal: 40-60°C
- High boost: 60-80°C
- >80°C = intercooler struggling

### Fuel System

**O2 Sensors** - Oxygen feedback.
- 0.4-0.6V = Rich (more fuel)
- 0.45V = Target AFR for your tune
- 0.7-0.9V = Lean (less fuel)

**Fuel Trim** - Correction factor.
- 0% = Perfect (target AFR achieved)
- Positive % = Engine richer than target
- Negative % = Engine leaner than target
- ±10% normal; >20% = tuning issue

### Transmission

**Current Gear** - Self-explanatory. P=Park, R=Reverse, D=Drive, etc.

**Trans Temp** - Fluid temperature.
- 40-60°C = Normal
- 80-100°C = Warm (after hard driving)
- >100°C = HOT (Proflow cooler should handle)
- >120°C = CRITICAL (pull over, cool down)

**Shift Pressure** - Transgo kit hydraulic pressure.
- Should rise smoothly under acceleration
- Hard lockup on WOT
- Pressure drop = valve body issues

**TCC Slip** - Torque converter clutch slippage.
- 0 RPM = Hard locked (as tuned)
- >100 RPM = Slipping (inefficient)
- Factory = 500+ RPM slip (comfort), tuned = hard lock for power

---

## Common Sensor Readings

### What's Normal?

**At Idle (1000 RPM, Engine Warm):**
```
RPM:                1000
Coolant:            90°C
Boost:              100 kPa (atmospheric)
Engine Load:        5-10%
Fuel Pressure:      450 kPa
Intake Temp:        45°C
Ignition Timing:    25° BTDC
Trans Temp:         60°C
O2 Sensor 1:        0.45V
Fuel Trim:          ±5%
```

**Cruising (2500 RPM, Moderate Load):**
```
RPM:                2500
Coolant:            92°C
Boost:              115 kPa
Engine Load:        20%
Fuel Pressure:      455 kPa
Intake Temp:        55°C
Ignition Timing:    22° BTDC
Trans Temp:         65°C
O2 Sensor 1:        0.45V
Fuel Trim:          ±3%
```

**Hard Acceleration (WOT, Boosted):**
```
RPM:                5000
Coolant:            96°C
Boost:              220 kPa (high boost!)
Engine Load:        95%
Fuel Pressure:      480 kPa (holding under load)
Intake Temp:        75°C (compressed air heating)
Ignition Timing:    12° BTDC (retarded for safety)
Trans Temp:         85°C (shifting hard)
O2 Sensor 1:        0.50V (richer for power)
Fuel Trim:          +8% (adding fuel)
```

---

## Alerts & What They Mean

| Alert | What It Means | What To Do |
|-------|---------------|-----------|
| 🔴 Coolant >105°C | Engine overheating | Slow down, let cool, check radiator |
| 🔴 Fuel Pressure <400 kPa | Pump failure risk | Check fuel filter, pump connections |
| 🔴 Trans Temp >120°C | Transmission too hot | Reduce load, enable cooler fan |
| 🟡 Boost >260 kPa | Excessive boost pressure | Check wastegate solenoid |
| 🟡 Fuel Trim ±25% | Major fueling correction | Check MAF/MAP sensor, injectors |
| 🟡 O2 Sensor 1 <0.3V | Lean condition | Check fuel pressure, injectors |
| 🟡 O2 Sensor 1 >0.8V | Rich condition | Check EFI Live tune, injector size |

---

## Frequently Asked Questions

**Q: Why is my boost only 100 kPa at idle?**  
A: That's normal! Atmospheric pressure is ~100 kPa. Boost only occurs under acceleration.

**Q: My fuel trim is +15%, is that bad?**  
A: Not necessarily. E85 runs richer than 98 octane. Check what fuel you're using.

**Q: Trans temp 95°C - should I be worried?**  
A: No, that's normal after hard driving. Proflow cooler handles that. Worry at 110°C+.

**Q: Why does ignition timing go negative?**  
A: It's retarded (delayed) for safety under boost. Negative values prevent detonation.

**Q: Can I tune my car with this app?**  
A: No, but you can monitor tuning changes in EFI Live. Export data to compare before/after.

**Q: What if device loses Bluetooth connection?**  
A: App auto-reconnects. If persistent, restart adapter and re-pair.

**Q: How long can I monitor?**  
A: As long as your vehicle runs. Phone needs power though (use car charger).

**Q: Can I use this with other vehicles?**  
A: No. App is locked to your E38 ECU via verification on first connection.

---

## Tips & Tricks

### Get More from Your Data

**1. Track Performance Over Time**
- Export session after each drive
- Compare boost curves session-to-session
- Spot trends (declining boost = boost leak?)

**2. Diagnose Issues**
- Export problematic session
- Send CSV to tuner with description
- Include fuel type (E85/98) in email

**3. Validate Tune Changes**
- Before: Export baseline data
- After: Make EFI Live tune change
- Export same session conditions
- Compare fuel trim, timing changes

**4. Monitor Health**
- Watch fuel pressure trend (should be stable)
- Monitor trans temp during spirited driving
- Track coolant temperature patterns

### Advanced Usage

**Real-Time Tuning Feedback**
1. Have someone monitor phone while you drive
2. Watch O2 sensors and fuel trim
3. Relay feedback for quick A/B tuning

**Dyno Data Correlation**
1. Export baseline dyno session
2. Export same vehicle on road
3. Compare boost curve and timing
4. Validate dyno vs real-world mapping

---

## Data Privacy

✅ **All data stays on your phone**  
✅ **No cloud uploads**  
✅ **No tracking**  
✅ **No ads**  

Data only leaves your device if you manually export and share files.

---

## Troubleshooting Quick Reference

| Problem | Solution |
|---------|----------|
| App won't connect | Restart adapter, re-pair Bluetooth |
| No PID response | Start engine, check OBD2 port |
| App crashes on startup | Clear app cache, reinstall |
| Bluetooth keeps dropping | Move away from WiFi, replace adapter battery |
| Export fails | Check storage permission, have 100MB free |
| Wrong vehicle alert | Confirm VIN matches car, ECU is E38 |

---

## Next Steps

1. ✅ **Install & Pair** - Follow Installation Quick Start
2. ✅ **First Connection** - Let app verify vehicle
3. ✅ **Live Monitoring** - Start engine, tap "Start Monitoring"
4. ✅ **Export Session** - Practice CSV export
5. ✅ **Analyze Data** - Open CSV in Excel or EFI Live
6. ✅ **Reference Guide** - Bookmark sensor meanings above

---

## Support Quick Links

**Can't Connect:**
- Ensure OBD2 adapter is in pairing mode
- Check Bluetooth is ON on phone
- Verify adapter power (should have light)

**Wrong Vehicle Error:**
- This app is locked to your specific E38 ECU
- Verify you're connecting to 2011 Holden VE Calais L77
- Contact app developer if verification fails

**Data Issues:**
- First 5 seconds of data may be unreliable (settling)
- For analysis, discard first reading
- Compare with EFI Live for verification

---

## Remember

⚠️ **Do not use while driving**  
⚠️ **Keep phone mounted safely**  
⚠️ **Some tests require track/dyno only**  
⚠️ **Always prioritize vehicle safety**

---

**Enjoy monitoring your build!**  
**2011 Holden VE Calais Redline L77**  
**Nathan Brookes (FOX95S)**

---

**Questions?** Refer to INSTALLATION_AND_SETUP.md for detailed guide  
**Lost?** Check the "What Each Parameter Means" section  
**Ready to tune?** Export your data and share with tuner!
