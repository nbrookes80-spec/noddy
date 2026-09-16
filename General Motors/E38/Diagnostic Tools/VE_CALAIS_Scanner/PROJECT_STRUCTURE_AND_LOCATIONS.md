# VE CALAIS V2.0.0 - Project Structure & File Locations

**Last Updated:** 2026-09-17  
**Primary Location:** `C:\Users\danod\OneDrive\Documents\ANDROID AP\`

---

## 📁 Directory Structure

```
C:\Users\danod\OneDrive\Documents\ANDROID AP/
│
├── 📄 Project Root Files
│   ├── build.gradle (root project config)
│   ├── settings.gradle
│   ├── gradle.properties (Java 23 compatibility settings)
│   └── gradlew (Gradle wrapper executable)
│
├── 📂 gradle/ (Gradle configuration)
│   └── wrapper/
│       └── gradle-wrapper.properties (Gradle 8.10.2)
│
├── 📂 app/ (Main application module)
│   ├── build.gradle (APP config - V2.0.0, versionCode=2)
│   ├── proguard-rules.pro (code obfuscation rules)
│   ├── 📂 src/
│   │   ├── main/
│   │   │   ├── AndroidManifest.xml (permissions, activities)
│   │   │   ├── 📂 java/com/brookes/ve_calais_obd2/
│   │   │   │   ├── MainActivity.kt (entry point)
│   │   │   │   ├── OBD2Protocol.kt (Mode 01/22 parsing)
│   │   │   │   ├── BluetoothManager.kt (ELM327 communication)
│   │   │   │   ├── BluetoothSession.kt (singleton session)
│   │   │   │   ├── PIDDatabase.kt (140+ PIDs, V2.0.0 enhanced)
│   │   │   │   ├── PIDParameter.kt (PID data class)
│   │   │   │   ├── SessionManager.kt (auto-logging)
│   │   │   │   ├── DataLogger.kt (CSV/JSON export)
│   │   │   │   ├── BluetoothConnectHelper.kt
│   │   │   │   ├── PidScanner.kt (DID sweep logic)
│   │   │   │   ├── Fragments/
│   │   │   │   │   ├── HomeFragment.kt (home screen)
│   │   │   │   │   ├── LiveDataFragment.kt (dashboard)
│   │   │   │   │   ├── DashboardPagerAdapter.kt (4-sensor pagination)
│   │   │   │   │   ├── PidScannerFragment.kt (scan interface)
│   │   │   │   │   ├── SnifferFragment.kt (raw traffic)
│   │   │   │   │   └── [other fragments]
│   │   │   │   └── [other .kt files]
│   │   │   │
│   │   │   └── 📂 res/ (Resources)
│   │   │       ├── 📂 values/
│   │   │       │   ├── strings.xml (app name="VE CALAIS", version="2.0.0")
│   │   │       │   ├── colors.xml
│   │   │       │   ├── dimens.xml
│   │   │       │   └── styles.xml
│   │   │       ├── 📂 layout/
│   │   │       │   ├── activity_main.xml
│   │   │       │   ├── fragment_home.xml
│   │   │       │   ├── fragment_live_data.xml
│   │   │       │   ├── item_pid_reading.xml (card layout)
│   │   │       │   ├── fragment_pid_scanner.xml
│   │   │       │   ├── fragment_sniffer.xml
│   │   │       │   └── [other layouts]
│   │   │       ├── 📂 mipmap/
│   │   │       │   ├── ic_launcher.png
│   │   │       │   └── ic_launcher_round.png
│   │   │       └── 📂 drawable/ (vector drawables, icons)
│   │   │
│   │   └── test/ (Unit tests, if any)
│   │
│   └── 📂 build/ (Build output - generated)
│       └── outputs/apk/debug/
│           └── app-debug.apk (V2.0.0, 1.45 MB)
│
├── 📂 .gradle/ (Gradle cache - auto-generated)
├── 📂 .idea/ (Android Studio project files)
└── 📂 [other project folders]
```

---

## 📦 APK Location & Distribution

### Primary APK
```
Path: C:\Users\danod\OneDrive\Documents\ANDROID AP\app\build\outputs\apk\debug\app-debug.apk
Size: 1.45 MB
Version: 2.0.0 (versionCode=2)
Status: ✅ Ready for installation
```

### Backup Copy (for easy access)
```
Path: C:\Users\danod\OneDrive\Documents\ANDROID AP\app-debug-v2.0.0.apk
Size: 1.45 MB (same file)
Status: ✅ Available for Google Drive download
```

---

## 📋 Documentation Files

### Version 2.0.0 Documentation (In Google Drive folder)
```
Location: C:\Users\danod\OneDrive\Documents\ANDROID AP\

Files:
├── V2.0.0_UPDATE_SUMMARY.md
│   └── Complete changelog, new PIDs, what's included
│
├── APP_TESTING_REPORT_V2.0.0.md
│   └── Build verification, structure checks, test status
│
├── PROJECT_STRUCTURE_AND_LOCATIONS.md (this file)
│   └── Directory layout, file locations, quick reference
│
├── DATABASE_UPDATE_SUMMARY.md
│   └── PID database changes, 22 new verified PIDs
│
├── VE_CALAIS_VERIFIED_PIDS.md
│   └── Comparison of 46 verified PIDs vs database
│
└── ve_calais_verified_pids_from_car.csv
    └── 46 verified PIDs in CSV format (importable)
```

---

## 🔧 Build Configuration Files

### Gradle Configuration
```
File: C:\Users\danod\OneDrive\Documents\ANDROID AP\build.gradle
Content:
  - Root project settings
  - Plugin versions
  - Java compatibility

File: C:\Users\danod\OneDrive\Documents\ANDROID AP\app\build.gradle
Content:
  ✅ versionCode = 2 (V2.0.0)
  ✅ versionName = "2.0.0"
  ✅ compileSdk = 34
  ✅ minSdk = 26
  ✅ targetSdk = 34
  ✅ All dependencies listed

File: C:\Users\danod\OneDrive\Documents\ANDROID AP\gradle.properties
Content:
  - JVM args: -Xmx4096m
  - Java 23 compatibility settings
  - Android X and Jetifier flags
```

### Gradle Wrapper
```
File: C:\Users\danod\OneDrive\Documents\ANDROID AP\gradle\wrapper\gradle-wrapper.properties
Version: gradle-8.10.2-bin.zip
```

---

## 🎯 Key Source Files

### Core Application Logic
```
OBD2Protocol.kt
  ├── parseRPM(), parseCoolantTemp(), parseMAP(), etc.
  ├── Mode 01 vs Mode 22 command formatting
  ├── Response parsing and validation
  └── Header routing (Auto, 7E0, 7E2, 7E3)

BluetoothManager.kt
  ├── ELM327 communication
  ├── Multi-line response handling
  ├── Synchronized I/O operations
  ├── Traffic callback for sniffer
  └── Demo mode simulation

PIDDatabase.kt (V2.0.0 - UPDATED)
  ├── 140+ PIDs total
  ├── 46 verified from scanExport.csv
  ├── MAP sensor: 0-300 kPa (3-bar scaling) ✅
  ├── TCM data: 7E2 header configuration ✅
  ├── getMonitoringPIDs() - 20 critical
  ├── getPerformancePIDs() - 17 advanced
  └── getDiagnosticPIDs() - 20 troubleshooting

SessionManager.kt
  ├── Auto-logging on connect
  ├── Session lifecycle management
  ├── Auto-save CSV/JSON on disconnect
  └── Timestamp-based file naming

DataLogger.kt
  ├── CSV export with headers
  ├── JSON export with metadata
  └── File I/O operations
```

### UI Fragments
```
HomeFragment.kt
  ├── Vehicle info display
  ├── Connection status
  ├── Quick navigation buttons
  └── Settings toggles

LiveDataFragment.kt (UPDATED)
  ├── 4-sensor dashboard
  ├── ViewPager2 pagination
  ├── Display mode cycling
  ├── Export buttons
  └── Demo mode support

DashboardPagerAdapter.kt
  ├── Page generation for ViewPager2
  ├── Card layout (100dp height)
  ├── Display modes: Digital, Graph, Histogram
  ├── History tracking (40 points per sensor)
  └── FrameLayout overlay system

PidScannerFragment.kt
  ├── DID sweep implementation
  ├── Scan plan selection
  ├── Real-time log display
  └── Export results

SnifferFragment.kt
  ├── Raw TX/RX capture
  ├── Timestamp logging
  └── Clear log button
```

### Resource Files
```
strings.xml (UPDATED)
  ├── app_name = "VE CALAIS" (was "VE Calais OBD2")
  ├── app_version = "2.0.0" (was "1.0.0")
  ├── Vehicle info strings
  ├── All UI text labels
  └── Message templates

AndroidManifest.xml
  ├── Package: com.brookes.ve_calais_obd2
  ├── Bluetooth permissions
  ├── Storage permissions
  ├── Location permission (for BT scanning)
  └── MainActivity as launcher

Layout XML Files
  ├── activity_main.xml - NavHostFragment container
  ├── fragment_home.xml - Home screen
  ├── fragment_live_data.xml - Dashboard container
  ├── item_pid_reading.xml - Card layout (updated)
  ├── fragment_pid_scanner.xml - Scanner UI
  └── fragment_sniffer.xml - Sniffer UI
```

---

## 🗂️ Removed Files (V2.0.0 Cleanup)

```
✅ Deleted: C:\Users\danod\OneDrive\Documents\01POWER OF ATTORNEY\ANDROID AP\
           (Old duplicate folder)

Status: Consolidated to single project location
```

---

## 📊 Database Content

### PIDDatabase.kt Location
```
File: C:\Users\danod\OneDrive\Documents\ANDROID AP\app\src\main\java\
      com\brookes\ve_calais_obd2\PIDDatabase.kt

Size: ~30 KB
Lines: 813
PIDs: 140+

Structure:
  ├── standardPidMap (Mode 01 & Mode 22 PIDs)
  ├── cylinderPidMap (per-cylinder data, V8: 8 cylinders)
  ├── buildCylinderPIDs() function
  ├── Helper functions:
  │   ├── getPIDsByCategory()
  │   ├── getPID()
  │   ├── getAllCategories()
  │   ├── getAllPIDs()
  │   ├── getMonitoringPIDs() (20 critical PIDs)
  │   ├── getPerformancePIDs() (17 advanced PIDs)
  │   └── getDiagnosticPIDs() (20 troubleshooting PIDs)
  └── init block for logging
```

### PID Categories
```
✅ Engine (25+ PIDs)
✅ Fuel (12+ PIDs)
✅ Turbo (3+ PIDs)
✅ Transmission (GM - Probable) (17+ PIDs)
✅ Transmission (Unverified) (3 placeholder PIDs)
✅ Electrical (2+ PIDs)
✅ Vehicle (1+ PID)
✅ Diagnostics (8+ PIDs)
✅ System (3+ PIDs)
```

---

## 🚀 Installation Instructions

### Step 1: Transfer APK to Phone
```
Option A (Google Drive):
  1. APK Location: C:\Users\danod\OneDrive\Documents\ANDROID AP\app-debug-v2.0.0.apk
  2. Open on phone → Google Drive app
  3. Download to phone storage
  4. Tap to install

Option B (USB Cable):
  1. APK Path: C:\Users\danod\OneDrive\Documents\ANDROID AP\app\build\outputs\apk\debug\app-debug.apk
  2. Connect Android device via USB
  3. Copy APK to device Downloads folder
  4. On phone: Files → Downloads → app-debug.apk → Install
```

### Step 2: Install on Android Device
```
1. Open APK file on phone
2. Allow installation from "Unknown Sources" if prompted
3. Grant permissions:
   ✅ Bluetooth
   ✅ Location (for Bluetooth scanning)
   ✅ Storage (for data logs)
4. Wait for installation complete
5. Launch "VE CALAIS" app
```

### Step 3: Initial Setup
```
1. Home Screen should display:
   - "VE CALAIS" title
   - Version "2.0.0"
   - Vehicle info: "2011 Holden VE Calais Redline L77"
   
2. Grant permissions when prompted:
   - Bluetooth scanning
   - Location access
   - File storage
   
3. Test Demo Mode (before connecting to car):
   - Home screen toggle "Demo Mode"
   - Go to Live Data
   - Should see simulated random-walk data
   - Test display modes (Digital → Graph → Histogram)
```

---

## 🔌 Connection to OBD2 Adapter

```
1. Hardware Setup:
   - Turn on ELM327 Bluetooth OBD2 adapter
   - Connect to car's OBD2 port (driver side, under dash)
   - Wait for Bluetooth indicator light

2. Phone Bluetooth:
   - Settings → Bluetooth
   - Search for ELM327
   - Pair (password usually 1234)

3. App Connection:
   - Open "VE CALAIS" app
   - Home screen → "Connect to OBD2 Adapter"
   - Select ELM327 from list
   - Status indicator should turn green
   - Auto-logging starts

4. Live Data:
   - Go to "Live Data" tab
   - Should see sensor readings
   - 4-sensor dashboard with pagination
   - Swipe left/right between pages
   - Tap cards to change display mode
```

---

## 📊 File Statistics

| File Type | Count | Location |
|-----------|-------|----------|
| Kotlin (.kt) | 20+ | src/main/java/ |
| XML Layout | 10+ | src/main/res/layout/ |
| Android Resources | 5+ | src/main/res/ |
| Gradle Configs | 4 | Root + gradle/ |
| Documentation | 8 | Project root |
| **Total** | **50+** | **Project folder** |

---

## 🔑 Quick Reference

### Android App Package
```
Package Name: com.brookes.ve_calais_obd2
Version Name: 2.0.0
Version Code: 2
Min SDK: 26 (Android 8.0)
Target SDK: 34 (Android 14)
Compile SDK: 34
```

### Key Directories
```
Project Root: C:\Users\danod\OneDrive\Documents\ANDROID AP\
Source Code: C:\Users\danod\OneDrive\Documents\ANDROID AP\app\src\main\java\
Resources: C:\Users\danod\OneDrive\Documents\ANDROID AP\app\src\main\res\
Build Output: C:\Users\danod\OneDrive\Documents\ANDROID AP\app\build\
APK Output: C:\Users\danod\OneDrive\Documents\ANDROID AP\app\build\outputs\apk\debug\
```

### Important Files
```
Build Config: C:\Users\danod\OneDrive\Documents\ANDROID AP\app\build.gradle
PID Database: C:\Users\danod\OneDrive\Documents\ANDROID AP\app\src\main\java\com\brookes\ve_calais_obd2\PIDDatabase.kt
Manifest: C:\Users\danod\OneDrive\Documents\ANDROID AP\app\src\main\AndroidManifest.xml
Strings: C:\Users\danod\OneDrive\Documents\ANDROID AP\app\src\main\res\values\strings.xml
APK File: C:\Users\danod\OneDrive\Documents\ANDROID AP\app\build\outputs\apk\debug\app-debug.apk
```

---

## ✅ Status Summary

| Item | Version | Status |
|------|---------|--------|
| App Name | VE CALAIS | ✅ Updated |
| Version Number | 2.0.0 | ✅ Updated |
| PID Database | 140+ | ✅ Enhanced |
| Verified PIDs | 46 | ✅ From car scan |
| Build Status | Clean | ✅ Success |
| APK Generated | 1.45 MB | ✅ Ready |
| Duplicate Project | Removed | ✅ Consolidated |

---

**Everything is organized and ready for testing on your 2011 Holden VE Calais!**

Questions? Check the other documentation files in the same folder:
- V2.0.0_UPDATE_SUMMARY.md
- APP_TESTING_REPORT_V2.0.0.md
- DATABASE_UPDATE_SUMMARY.md
- VE_CALAIS_VERIFIED_PIDS.md
