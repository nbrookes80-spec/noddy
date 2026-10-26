[app]
title = TunerToolPro
package.name = tunertoolpro
package.domain = org.tunertoolpro
source.dir = .
source.include_exts = py
source.exclude_dirs = tests, __pycache__
version = 0.1.0
requirements = python3,kivy,pyjnius
p4a.branch = v2024.01.21
orientation = portrait
fullscreen = 0
android.archs = arm64-v8a, armeabi-v7a
android.minapi = 24
android.allow_backup = True
# Wi-Fi scan adapter needs INTERNET. Bluetooth Classic needs the BLUETOOTH permissions;
# Android 12 and later uses BLUETOOTH_CONNECT and BLUETOOTH_SCAN at run time.
android.permissions = INTERNET, BLUETOOTH, BLUETOOTH_ADMIN, BLUETOOTH_CONNECT, BLUETOOTH_SCAN, ACCESS_FINE_LOCATION

[buildozer]
log_level = 2
warn_on_root = 1
