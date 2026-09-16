# VE Calais L77 OBD2 Live Data Reader
## Android Application for 2011 Holden VE Calais Redline / Pontiac G8

**Owner:** Nathan Brookes  
**Vehicle:** 2011 Holden VE Calais Redline L77  
**ECU:** E38  
**Fuel:** E85/98 Flex  
**MAP Sensor:** 2.7 Bar  
**Build Date:** July 28, 2026

---

## Features

✅ **Vehicle-Specific Configuration** - Locked to E38 ECU via VIN verification  
✅ **Bluetooth OBD2 Connection** - Seamless ELM adapter connectivity  
✅ **Real-Time Live Data Display** - 50+ sensor readings simultaneously  
✅ **E38-Specific PID Database** - Custom calibrated for your turbo L77 build  
✅ **Turbo Monitoring** - Boost pressure, MAP sensor, intake temps  
✅ **Transmission Monitoring** - 6L80E shift pressures, TCC lockup, temps  
✅ **Fuel System** - Fuel pressure, injector pulsewidth, AFR, O2 sensors  
✅ **Engine Management** - Ignition timing, load, cylinder airmass, VE  
✅ **Data Logging** - Export CSV/JSON for tuning analysis  
✅ **Customizable Dashboard** - Select your monitored parameters  
✅ **Alerts & Warnings** - Critical threshold notifications  
✅ **No Other Vehicle Support** - E38 ECU verification only

---

## Installation

### Prerequisites
- Android 8.0+ (API 26)
- Bluetooth Low Energy capable device
- ELM327 or compatible OBD2 Bluetooth adapter
- Vehicle must be 2011 Holden VE Calais or Pontiac G8 equivalent

### Build Instructions
1. Clone/extract the project files
2. Open in Android Studio (Arctic Fox or later)
3. Connect Android device with USB debugging enabled
4. Run `./gradlew build`
5. Install via `./gradlew installDebug`

---

## Hardware Requirements

- **OBD2 ELM Adapter:** Any Bluetooth ELM327 module
- **Pairing:** Pair adapter via Android Bluetooth settings first
- **Power:** Ensure OBD2 adapter powered (via 12V vehicle power)

---

## Usage

1. **Launch App** → Select Bluetooth device
2. **Vehicle Verification** → App confirms E38 ECU (VIN/ECU ID check)
3. **Live Data Screen** → Real-time sensor readings
4. **Select Parameters** → Customize which sensors display
5. **Data Logging** → Record session for later analysis
6. **Export** → Save as CSV for tuning software

---

## App Structure

```
VE_Calais_OBD2/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/brookes/ve_calais_obd2/
│   │   │   │   ├── MainActivity.kt
│   │   │   │   ├── BluetoothManager.kt
│   │   │   │   ├── OBD2Protocol.kt
│   │   │   │   ├── PIDDatabase.kt
│   │   │   │   ├── VehicleVerification.kt
│   │   │   │   ├── LiveDataFragment.kt
│   │   │   │   ├── SettingsFragment.kt
│   │   │   │   └── DataLogger.kt
│   │   │   ├── res/
│   │   │   │   ├── layout/
│   │   │   │   ├── values/
│   │   │   │   └── drawable/
│   │   │   └── AndroidManifest.xml
│   │   └── test/
│   └── build.gradle
└── gradle/

```

---

## Key Customizations for Your Build

### E38 ECU Specifics
- Double Stoich / Half Flow injector scaling (KPM1500)
- Flex Fuel AFR tables (E85 compensation)
- Speed Density with 2.7 Bar MAP sensor
- MAF zeroed out (P0101, P0102, P0103)
- Torque management 30% scaling
- 3.9 differential ratio gear scaling
- TCC lockup zero slip for Circle D triple disk

### Monitored Systems
- **Engine:** RPM, Load, Timing, Cylinder Air Mass, VE
- **Fuel:** Pressure, Trim (Short/Long), AFR, O2 sensors
- **Boost:** MAP pressure (2.7 bar sensor), intake temp
- **Transmission:** Shift pressures, TCC slip, gear, temp
- **Cooling:** Coolant temp, Oil temp, Intercooler temp
- **Electrical:** Battery voltage, Alternator load

---

## PID Reference for E38 ECU

| Parameter | PID | Range | Unit |
|-----------|-----|-------|------|
| Engine RPM | 010C | 0-8000 | RPM |
| Coolant Temp | 0105 | -40-125 | °C |
| Fuel Pressure (Relative) | 010A | 0-765 | kPa |
| MAP Sensor | 010B | 0-270 | kPa |
| Ignition Timing | 011E | -64-64 | °BTDC |
| O2 Sensor 1 | 0114 | 0-1.275 | V |
| O2 Sensor 2 | 0115 | 0-1.275 | V |
| Short Term Fuel Trim B1 | 0106 | -100-100 | % |
| Long Term Fuel Trim B1 | 0107 | -100-100 | % |
| Intake Air Temp | 010F | -40-215 | °C |
| Absolute Load | 0143 | 0-25500 | % |
| Transmission Fluid Temp | 01F0 | -40-125 | °C |

*Additional 70+ parameters available in app database*

---

## Vehicle Verification

The app verifies your vehicle via:
1. **VIN Check** - Confirms 2011 model year, Holden/Pontiac
2. **ECU ID Request** - Confirms E38 ECU module
3. **Hardware Signature** - Validates turbo build signature
4. **One-time Setup** - Locks to your vehicle permanently

---

## Data Export

Sessions can be exported as:
- **CSV** - Compatible with Excel, tuning software
- **JSON** - For custom analysis tools
- **PDF Report** - Session summary with graphs

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Device Not Recognized" | Verify VIN matches vehicle ECU |
| "No Bluetooth Connection" | Pair adapter in Android settings first |
| "PID Not Responding" | Check ELM adapter serial connection |
| "Boost Reading Wrong" | Verify 2.7 Bar MAP sensor calibration in app |
| "Fuel Pressure Erratic" | Confirm KPM pump module 500 kPa pressure |

---

## Important Notes

⚠️ **This app only works with:**
- 2011 Holden VE Calais Redline L77
- 2011 Pontiac G8 (USA equivalent)
- E38 ECU with matching hardware signature

⚠️ **Safety Warning:**
- Do not use while driving
- Some parameters require WOT testing on track only
- Monitor critical sensors before aggressive tuning
- Refer to your EFI Live tune for confirmed values

---

## Support

For technical issues or questions about your specific build configuration, refer to the engineering certification document included with your files.

**Owner:** Nathan Brookes (FOX95S)  
**Created:** July 2026
