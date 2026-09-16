# VE Calais L77 OBD2 Reader - Installation & Setup Guide

**App Version:** 1.0.0  
**Target:** Android 8.0+ (API 26)  
**Vehicle:** 2011 Holden VE Calais Redline L77 (Pontiac G8)  
**Owner:** Nathan Brookes (FOX95S)

---

## Prerequisites

### Hardware Requirements
1. **Android Phone/Tablet**
   - Android 8.0 or higher
   - Bluetooth 4.0+ capability
   - Minimum 200 MB free storage
   - Recommended: 6" screen or larger for data visibility

2. **OBD2 Adapter**
   - Bluetooth ELM327 (or compatible)
   - Must support ISO 14230-4 (KWP2000) protocol
   - Recommended: iCarsoft or Viecar branded adapter
   - Power source: Vehicle 12V OBD2 port

3. **Vehicle**
   - 2011 Holden VE Calais Redline
   - E38 ECU (app verifies automatically)
   - Engine must be running for live data

### Software Requirements
- Android Studio (Arctic Fox or later)
- JDK 11 or higher
- Gradle 7.0+
- Git (optional, for cloning)

---

## Installation Steps

### Step 1: Prepare the Project Files

Extract all provided files into a single directory:
```
VE_Calais_OBD2/
├── app/
│   ├── src/main/
│   │   ├── java/com/brookes/ve_calais_obd2/
│   │   │   ├── MainActivity.kt
│   │   │   ├── BluetoothManager.kt
│   │   │   ├── OBD2Protocol.kt
│   │   │   ├── PIDDatabase.kt
│   │   │   ├── VehicleVerification.kt
│   │   │   ├── DataLogger.kt
│   │   │   └── ui/
│   │   │       └── LiveDataFragment.kt
│   │   ├── res/
│   │   │   ├── layout/
│   │   │   │   ├── activity_main.xml
│   │   │   │   └── fragment_live_data.xml
│   │   │   └── values/
│   │   │       └── strings.xml
│   │   └── AndroidManifest.xml
│   └── build.gradle
├── build.gradle (project-level)
├── settings.gradle
└── README.md
```

### Step 2: Open in Android Studio

1. Launch Android Studio
2. Select "Open an existing Android Studio project"
3. Navigate to the `VE_Calais_OBD2` directory
4. Click "Open"
5. Wait for Gradle sync to complete

### Step 3: Configure SDK and Build Tools

1. Go to `File > Project Structure`
2. Ensure SDK is set to API 34 (latest stable)
3. Build Tools version: 34.0.0 or higher
4. Click "Sync Now"

### Step 4: Build the App

**Via Android Studio:**
1. Select `Build > Build Bundle(s) / APK(s) > Build APK(s)`
2. Wait for build to complete
3. Locate APK in `app/build/outputs/apk/debug/`

**Via Command Line:**
```bash
cd VE_Calais_OBD2
./gradlew build
```

### Step 5: Deploy to Device

**Option A: Direct Connection (Recommended)**
1. Enable USB Debugging on Android device:
   - Settings > About Phone > Tap Build Number 7 times
   - Go back > System > Developer Options > USB Debugging: ON
2. Connect device to computer via USB
3. In Android Studio: `Run > Run 'app'`
4. Select your device and click OK

**Option B: Manual APK Installation**
1. After build completes, locate the APK
2. Transfer to your Android device (USB, email, etc.)
3. Open file manager on device
4. Tap the APK file to install
5. Follow installation prompts

**Option C: ADB Command Line**
```bash
adb connect <device_ip>  # If wireless
adb install app/build/outputs/apk/debug/app-debug.apk
```

---

## Post-Installation Setup

### 1. Grant Permissions

When you first launch the app, it will request permissions:
- ✅ **Bluetooth** - Required for OBD2 connection
- ✅ **Location** - Required by Android for Bluetooth scanning
- ✅ **Storage** - Required for data logging export

**Grant all permissions** for full functionality.

### 2. Pair OBD2 Adapter

1. On your Android device, go to Settings > Bluetooth
2. Turn Bluetooth ON
3. Put your OBD2 adapter in pairing mode (consult adapter manual)
4. Select the adapter from "Available Devices"
5. Pairing PIN (if asked): typically `0000` or `1234`
6. Adapter should now appear in "Paired Devices"

### 3. Launch VE Calais OBD2 App

1. Tap the app icon on your home screen
2. On first launch, you'll see the vehicle verification screen
3. The app will attempt to auto-connect to your OBD2 adapter
4. Navigate to "Live Data" tab

### 4. Vehicle Verification (First Connection)

The app verifies your vehicle via:
1. **VIN Check** - Requests VIN from ECU (Service 0x09)
2. **ECU ID Check** - Confirms E38 ECU module
3. **Build Verification** - Optional MAP sensor check

**Expected verification output:**
```
Owner: Nathan Brookes (FOX95S)
Vehicle: 2011 Holden VE Calais Redline
Engine: L77 6.0L V8 (DOD Deleted)
ECU: E38
Fuel: E85/98 Flex
Turbo: Killaboost G42-1450 (2.7 Bar MAP)
Transmission: 6L80E with Transgo Kit
```

✅ If verification passes → App is now locked to your vehicle  
❌ If verification fails → Check OBD2 connection and ECU compatibility

### 5. Start Live Monitoring

1. Start your vehicle engine
2. Tap "Start Monitoring" button
3. App will begin scanning PIDs every 500ms
4. Live readings appear in real-time

---

## Usage Guide

### Live Data Screen

The main dashboard displays four categories:

**Engine Parameters**
- RPM, Coolant Temp, IAT, Engine Load
- MAP (Boost), Fuel Pressure, Ignition Timing
- Vehicle Speed

**Fuel System**
- O2 Sensor voltages
- Short/Long term fuel trim
- Fuel pressure readings

**Transmission (6L80E)**
- Current gear selection
- Transmission fluid temperature
- Shift pressure
- TCC slip speed

**Monitoring Controls**
- Start/Stop monitoring
- Select PID category
- Export data

### Data Logging

The app automatically logs all monitored parameters. To export:

1. **Stop Monitoring** (button turns red)
2. Tap **Export CSV** or **Export JSON**
3. Files saved to: `/storage/emulated/0/Documents/VECalaisLogs/`

### Performance Monitoring Mode

To enter performance mode for WOT testing:
1. Navigate to **Settings** tab
2. Enable "Performance Monitoring"
3. Select "Performance PIDs" from category filter
4. Start monitoring
5. Perform WOT run
6. Export data for analysis with EFI Live

---

## File Locations & Exports

### App Data Directory
```
Internal Storage/
└── Android/
    └── data/
        └── com.brookes.ve_calais_obd2/
            └── files/
                └── Documents/
                    └── VECalaisLogs/
                        ├── VE_Calais_20260728_145230.csv
                        ├── VE_Calais_20260728_145230.json
                        └── VE_Calais_20260728_145230_Report.txt
```

### Export File Formats

**CSV Format** - Compatible with Excel, tuning software
```
VE Calais L77 OBD2 Data Log
Owner,Nathan Brookes
Vehicle,2011 Holden VE Calais Redline
Engine,L77 6.0L V8
ECU,E38
Session ID,d4f3c8a2-1234-5678-90ab-cdef12345678

Timestamp,RPM,Coolant Temp,Boost,Fuel Pressure,...
2026-07-28 14:52:30,1200,85,101,450,...
2026-07-28 14:52:31,1215,85,102,451,...
```

**JSON Format** - For data analysis tools
```json
{
  "sessionId": "d4f3c8a2-1234-5678-90ab-cdef12345678",
  "startTime": 1690548750000,
  "endTime": 1690548950000,
  "owner": "Nathan Brookes",
  "vehicle": "2011 Holden VE Calais Redline",
  "engineModel": "L77 6.0L V8",
  "ecuId": "E38",
  "entries": [
    {
      "timestamp": 1690548750100,
      "data": {
        "RPM": 1200,
        "CoolantTemp": 85,
        "Boost": 101,
        "FuelPressure": 450
      }
    }
  ]
}
```

**PDF Report** - Human-readable session summary
```
════════════════════════════════════════════════════════════════════════════════
VE CALAIS L77 OBD2 DATA SESSION REPORT
════════════════════════════════════════════════════════════════════════════════

VEHICLE INFORMATION
────────────────────────────────────────────────────────────────────────────────
Owner: Nathan Brookes
Vehicle: 2011 Holden VE Calais Redline
Engine: L77 6.0L V8
ECU: E38
...
```

---

## Troubleshooting

### "Device Not Found"
- Verify OBD2 adapter is paired in Bluetooth settings
- Check adapter power (should have LED indicator)
- Restart adapter and app
- Try different Bluetooth adapter if available

### "Vehicle Not Recognized"
- Confirm you're connecting to correct vehicle
- Check ECU module is E38
- Verify VIN matches 2011 Holden VE Calais
- Try factory reset if device was reprogrammed

### "No PID Response"
- Ensure engine is RUNNING (key in ON position minimum)
- Check OBD2 port for loose connections
- Try different PIDs first (RPM usually responds first)
- Restart adapter and device

### "Bluetooth Constantly Disconnecting"
- Move away from WiFi routers
- Ensure adapter has good power supply
- Update adapter firmware if available
- Replace adapter if issue persists

### "App Crashes on Launch"
- Clear app cache: Settings > Apps > VE Calais OBD2 > Storage > Clear Cache
- Uninstall and reinstall app
- Ensure Android OS is fully updated
- Check Android version is 8.0 or higher

### "Data Not Exporting"
- Enable file permissions: Settings > Apps > VE Calais OBD2 > Permissions
- Check device storage has >100MB free
- Ensure Documents folder exists on device
- Restart app and try export again

---

## Performance Tuning Data Analysis

Your exported data can be imported into:
- **EFI Live** - Tuning software (.csv compatible)
- **Microsoft Excel** - Data analysis (.csv)
- **Custom Python Scripts** - Data processing (.json)
- **Google Sheets** - Cloud analysis (.csv)

### Example: Import to EFI Live
1. Export session as CSV
2. Open EFI Live tuning software
3. Tools > Data Logger > Import External Log
4. Select your CSV file
5. View real-time engine parameters overlaid with tune

### Example: Python Data Analysis
```python
import json
import pandas as pd

with open('VE_Calais_20260728_145230.json') as f:
    data = json.load(f)

df = pd.DataFrame([e['data'] for e in data['entries']])
print(df.describe())  # Statistical summary
```

---

## Advanced Features

### Custom PID Scanning

Edit `PIDDatabase.kt` to add custom E38 PIDs:
```kotlin
"01FF" to PIDParameter(
    pid = "01FF",
    name = "Custom Parameter",
    category = "Custom",
    unit = "Units",
    min = 0.0,
    max = 100.0,
    description = "Custom sensor reading"
)
```

### Alerts & Warnings

Configure threshold alerts in `MainActivity.kt`:
```kotlin
// Alert if coolant temp > 95°C
if (coolantTemp > 95.0) {
    showCriticalAlert("COOLANT TEMPERATURE HIGH", coolantTemp)
}

// Alert if fuel pressure < 400 kPa
if (fuelPressure < 400.0) {
    showWarningAlert("LOW FUEL PRESSURE", fuelPressure)
}
```

### Data Streaming

For real-time data to cloud/web:
```kotlin
// In LiveDataFragment.kt, add to updateUIWithReadings()
val sessionData = mapOf(
    "timestamp" to System.currentTimeMillis(),
    "readings" to pidReadings
)
// Send to your server/cloud service
```

---

## Support & Troubleshooting Resources

**Bluetooth Connection Issues:**
- Verify adapter is powered from OBD2 port
- Check Android Bluetooth settings for pairing
- Try "Forget Device" and re-pair if persistent issues

**OBD2 Protocol:**
- E38 ECU uses ISO 14230-4 (KWP2000)
- App auto-sets correct protocol
- If manual: ELM adapter `AT SP6` = KWP2000

**Data Accuracy:**
- First 5-10 seconds of data may be unreliable
- Wait for engine to stabilize before analysis
- Compare with EFI Live datalog for verification

**Performance:**
- App updates every 500ms by default
- Slower devices may update every 1000ms
- Reduce PID count for older phones
- Disable data logging on slower devices

---

## Support Contact

For technical issues specific to your build configuration:
- Owner: Nathan Brookes (FOX95S)
- Vehicle: 2011 Holden VE Calais Redline L77
- Refer to engineering certification document for build specs

---

## Version History

**v1.0.0 (July 2026)**
- Initial release
- 50+ E38 ECU-specific PIDs
- Live data monitoring
- CSV/JSON data export
- Vehicle verification lock
- 6L80E transmission monitoring
- Turbo boost monitoring
- Fuel system monitoring

---

## License & Disclaimer

⚠️ **SAFETY WARNING:**
This app is provided for diagnostic and monitoring purposes only. Do not use while driving. Some parameters may only be checked safely on a dyno or closed track.

Always prioritize vehicle safety. When in doubt, consult professional tuning specialists.

---

**Built for:** 2011 Holden VE Calais Redline L77  
**Locked to:** E38 ECU Verification  
**Owner:** Nathan Brookes (FOX95S)  
**Created:** July 28, 2026
