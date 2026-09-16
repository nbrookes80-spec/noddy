# VE Calais E38 ECU - VERIFIED WORKING PIDs

## Your Scan Results: Real Data from Your Car! 🎯

**Source:** scanExport.csv from your E38 ECU  
**Header:** 7E0 (ECM)  
**Mode:** 01 (Standard SAE PIDs)  
**Working PIDs:** 46 confirmed responding  
**Unsupported PIDs:** 199 (got "Service Not Supported" response)

---

## Working PIDs (46 Total)

| PID Code | SAE Standard Name | Status | Notes |
|----------|-------------------|--------|-------|
| 0x0000 | PID Support 00-20 | ✅ WORKS | Bitmap of supported PIDs |
| 0x0001 | Monitor Status | ✅ WORKS | DTC and test status |
| 0x0003 | Fuel System Status | ✅ WORKS | Open/closed loop, etc |
| 0x0004 | Calculated Load | ✅ WORKS | Engine load % |
| 0x0005 | Coolant Temperature | ✅ WORKS | **Critical parameter** |
| 0x0006 | Short Term Fuel Trim B1 | ✅ WORKS | Fuel correction bank 1 |
| 0x0007 | Long Term Fuel Trim B1 | ✅ WORKS | Fuel correction bank 1 |
| 0x0008 | Short Term Fuel Trim B2 | ✅ WORKS | Fuel correction bank 2 |
| 0x0009 | Long Term Fuel Trim B2 | ✅ WORKS | Fuel correction bank 2 |
| 0x000A | Fuel Pressure | ✅ WORKS | Fuel rail pressure |
| 0x000B | Intake Manifold Pressure (MAP) | ✅ WORKS | **Critical - boost reading** |
| 0x000C | Engine RPM | ✅ WORKS | **Core parameter** |
| 0x000D | Vehicle Speed | ✅ WORKS | Speed from ECU |
| 0x000E | Ignition Timing Advance | ✅ WORKS | Spark timing |
| 0x000F | Intake Air Temperature | ✅ WORKS | IAT sensor |
| 0x0010 | Mass Air Flow | ✅ WORKS | MAF sensor (speed density tune) |
| 0x0011 | Throttle Position | ✅ WORKS | TPS % |
| 0x0013 | O2 Sensor 1 (B1S1) Voltage | ✅ WORKS | Upstream O2 sensor |
| 0x0014 | O2 Sensor 2 (B1S2) Voltage | ✅ WORKS | Downstream O2 sensor |
| 0x0015 | O2 Sensor 3 (B2S1) Voltage | ✅ WORKS | Bank 2 upstream O2 |
| 0x0018 | O2 Sensors Present | ✅ WORKS | O2 sensor count/type |
| 0x0019 | Aux Input Status | ✅ WORKS | Auxiliary inputs |
| 0x001C | OBD Standards Compliance | ✅ WORKS | Standards version |
| 0x001F | Runtime Since Engine Start | ✅ WORKS | Seconds running |
| 0x0020 | PID Support 21-40 | ✅ WORKS | Bitmap continued |
| 0x0021 | Distance with MIL On | ✅ WORKS | Check engine distance |
| 0x002E | Commanded Evaporative Purge | ✅ WORKS | EVAP purge % |
| 0x002F | Fuel Tank Level | ✅ WORKS | Fuel gauge reading |
| 0x0030 | Number of Warm-ups | ✅ WORKS | Warm-up cycles |
| 0x0031 | Distance Since DTC Cleared | ✅ WORKS | Distance counter |
| 0x0032 | Evaporative System Vapor Pressure | ✅ WORKS | EVAP pressure |
| 0x0033 | Barometric Pressure | ✅ WORKS | Atmospheric pressure |
| 0x003C | Catalyst Temperature B1S1 | ✅ WORKS | Cat temp sensor |
| 0x003D | Catalyst Temperature B2S1 | ✅ WORKS | Cat temp sensor |
| 0x0040 | PID Support 41-60 | ✅ WORKS | Bitmap continued |
| 0x0041 | Monitor Status This Drive Cycle | ✅ WORKS | Monitor flags |
| 0x0042 | Control Module Voltage | ✅ WORKS | Battery voltage |
| 0x0043 | Absolute Load Value | ✅ WORKS | Engine load (alternate) |
| 0x0044 | Commanded Air-Fuel Ratio | ✅ WORKS | A/F ratio command |
| 0x0045 | Relative Throttle Position | ✅ WORKS | Relative TPS % |
| 0x0046 | Ambient Air Temperature | ✅ WORKS | Outside air temp |
| 0x0047 | Absolute Throttle Position D | ✅ WORKS | Throttle position |
| 0x0049 | Accelerator Pedal D | ✅ WORKS | Pedal position |
| 0x004A | Accelerator Pedal E | ✅ WORKS | Pedal position |
| 0x004C | Commanded Throttle Position | ✅ WORKS | Commanded TPS |
| 0x0052 | Ethanol Fuel % | ✅ WORKS | **E85/98 Flex Fuel** |

---

## Comparison with sample_custom_pids.csv

### ✅ Already in Our Database (22 PIDs)

These are already in `sample_custom_pids.csv`:
- 0x0105 (Coolant Temperature)
- 0x010B (MAP Sensor)
- 0x010C (Engine RPM)
- 0x010D (Vehicle Speed)
- 0x010E (Ignition Timing)
- 0x010F (Intake Air Temperature)
- 0x0110 (MAF Air Flow)
- 0x0111 (Throttle Position)
- 0x0114 (O2 Sensor 1)
- 0x0115 (O2 Sensor 2)
- 0x012F (Fuel Tank Level)
- 0x0142 (Control Module Voltage)
- 0x0143 (Engine Load)
- 0x0152 (Ethanol Fuel %)
- 0x015C (Oil Temperature - if supported)
- 0x0146 (Ambient Air Temperature)
- 0x010A (Fuel Pressure)
- 0x0104 (Calculated Load)
- 0x0106 (Short Fuel Trim B1)
- 0x0107 (Long Fuel Trim B1)
- 0x0108 (Short Fuel Trim B2)
- 0x0109 (Long Fuel Trim B2)

### 🆕 New Discoveries (24 PIDs NOT in our database!)

These PIDs **work on your car but aren't in sample_custom_pids.csv**:
- 0x0000 - PID Support 00-20 (bitmap)
- 0x0001 - Monitor Status
- 0x0003 - Fuel System Status
- 0x0011 - Throttle Position (alternate)
- 0x0013 - O2 Sensor 3 (B2S1)
- 0x0018 - O2 Sensors Present
- 0x0019 - Aux Input Status
- 0x001C - OBD Standards Compliance
- 0x001F - Runtime Since Engine Start ⭐
- 0x0020 - PID Support 21-40 (bitmap)
- 0x0021 - Distance with MIL On
- 0x002E - Commanded Evaporative Purge
- 0x002F - Fuel Tank Level (alternate)
- 0x0030 - Number of Warm-ups
- 0x0031 - Distance Since DTC Cleared
- 0x0032 - Evaporative System Vapor Pressure
- 0x0033 - Barometric Pressure ⭐
- 0x003C - Catalyst Temperature B1S1
- 0x003D - Catalyst Temperature B2S1
- 0x0040 - PID Support 41-60 (bitmap)
- 0x0041 - Monitor Status This Drive Cycle
- 0x0043 - Absolute Load Value (alternate)
- 0x0044 - Commanded Air-Fuel Ratio
- 0x0045 - Relative Throttle Position
- 0x0047 - Absolute Throttle Position
- 0x0049 - Accelerator Pedal Position D
- 0x004A - Accelerator Pedal Position E
- 0x004C - Commanded Throttle Position

---

## Key Findings

### ✨ CRITICAL - This Is YOUR Real Data!

Your `scanExport.csv` is **GOLD** because it proves what actually works on your E38 ECU. This is better than any generic database.

### 🎯 High-Value New PIDs to Add

These 24 new PIDs are verified working and valuable:

1. **0x001F - Runtime Since Engine Start** ⭐
   - Useful for tracking session duration
   - Category: Engine
   - Formula: (A*256)+B (16-bit value in seconds)

2. **0x0033 - Barometric Pressure** ⭐
   - Critical for boost calculations
   - Category: Turbo/Sensors
   - Formula: A * 1 (kPa)

3. **0x0021 - Distance with MIL On**
   - Diagnostic tracking
   - Category: Diagnostics
   - Formula: (A*256)+B (16-bit km)

4. **0x003C / 0x003D - Catalyst Temperatures**
   - Monitor turbo/boost effects on exhaust
   - Category: Engine
   - Formula: ((A*256)+B)/10 (Celsius)

### ❌ PIDs That DON'T Work (199 unsupported)

Many standard PIDs returned "Service Not Supported" - this is normal as not all OBD2 vehicles support every PID. Your E38 just has a different subset.

---

## About the VAT Files

**HLKVV0GB.VAT** and **AUDVJ0GB.VAT** are Snap-on proprietary binary diagnostic calibration files. They're encrypted/compressed and would require Snap-on's proprietary tools to decode. **However, you don't need them** - your `scanExport.csv` is the actual verified data, which is better!

---

## Recommendations

### Add to Android App (24 New PIDs)

Create an updated CSV with these working PIDs:
```
PID,Name,Category,Unit,Min,Max,Description,Header,Formula
001F,Runtime Since Start,Engine,seconds,0,2147483,Time since engine started,Auto,(A*256)+B
0033,Barometric Pressure,Sensors,kPa,0,255,Atmospheric pressure baseline,Auto,A
003C,Catalyst Temp B1S1,Engine,°C,0,655,Catalyst temperature bank 1,Auto,((A*256)+B)/10
003D,Catalyst Temp B2S1,Engine,°C,0,655,Catalyst temperature bank 2,Auto,((A*256)+B)/10
...
```

### Test These First (Priority)

Start with the most useful ones:
1. **0x010C** - RPM (core)
2. **0x0105** - Coolant Temp (core)
3. **0x010B** - MAP/Boost (critical for turbo)
4. **0x0033** - Barometric Pressure (for boost delta)
5. **0x0152** - Ethanol % (E85/98 fuel)

All 46 should work, but start with these to verify your OBD2 adapter and the app fixes are working correctly.

---

## Next Steps

1. ✅ **Verify your APK works** with these known-good PIDs
2. 📊 **Add the 24 new PIDs** to your app's database
3. 🧪 **Test with real car** - all 46 should respond
4. 📝 **Document which ones are most useful** for your monitoring

**Your car is providing comprehensive OBD2 data - 46 working PIDs is excellent!**
