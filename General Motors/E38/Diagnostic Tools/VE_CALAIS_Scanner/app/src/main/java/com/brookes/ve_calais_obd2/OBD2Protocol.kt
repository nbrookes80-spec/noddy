package com.brookes.ve_calais_obd2

import timber.log.Timber

class OBD2Protocol(private val bluetoothManager: BluetoothManager) {

    /**
     * Request a PID value from the vehicle. Switches the CAN header first if this PID
     * needs a specific module address (GM enhanced/Mode 22 PIDs) rather than the default.
     * Formats the command properly: Mode 01 is "01XX", Mode 22 is "22XXXX".
     * Returns just the data bytes without the mode/PID echo.
     */
    fun requestPID(pidParam: PIDParameter): String? {
        return try {
            bluetoothManager.setHeader(pidParam.header)

            // Format the command: Mode 01 for "01XX" PIDs, Mode 22 for "22XXXX"
            val command = if (pidParam.pid.startsWith("22")) {
                "22${pidParam.pid.substring(2)}"  // Mode 22: "22XXXX"
            } else {
                pidParam.pid  // Mode 01: "01XX"
            }

            val fullResponse = bluetoothManager.sendCommand(command) ?: return null

            if (fullResponse.contains("UNABLE TO CONNECT") || fullResponse.contains("NO DATA")
                || fullResponse.contains("BUS ERROR") || fullResponse.isEmpty()) {
                Timber.w("No data for PID: ${pidParam.pid} - response: $fullResponse")
                return null
            }

            // Remove all whitespace and convert to uppercase for parsing
            val cleanResponse = fullResponse.replace("\\s+".toRegex(), "").uppercase()

            // Extract just the data bytes (skip mode echo)
            // Mode 01 response format: 41XX[data...]
            // Mode 22 response format: 62XX[data...]
            val dataBytes = when {
                cleanResponse.startsWith("41") && command.startsWith("01") -> {
                    cleanResponse.substring(4)  // Skip "41XX"
                }
                cleanResponse.startsWith("62") && command.startsWith("22") -> {
                    cleanResponse.substring(4)  // Skip "62XX"
                }
                else -> cleanResponse
            }

            if (dataBytes.isEmpty()) {
                Timber.w("Empty data for PID: ${pidParam.pid}")
                return null
            }

            Timber.d("PID ${pidParam.pid}: raw=$fullResponse -> data=$dataBytes")
            dataBytes
        } catch (e: Exception) {
            Timber.e(e, "Error requesting PID: ${pidParam.pid}")
            null
        }
    }

    /**
     * Request Vehicle Identification Number (VIN)
     * Service 0x09 (Request Vehicle Info)
     */
    fun requestVIN(): String? {
        bluetoothManager.setHeader("Auto")
        return bluetoothManager.sendCommand("0902")
    }

    /**
     * Request ECU Name/ID
     * Service 0x09, Data ID 0x0A
     */
    fun requestECUID(): String? {
        bluetoothManager.setHeader("Auto")
        return bluetoothManager.sendCommand("090A")
    }

    /**
     * Reads stored/confirmed DTCs via standard SAE J1979 Mode 03 - this is the legacy OBD2
     * service every emissions-compliant vehicle (including this one) supports on the public
     * OBD2 port, so it's the reliable read path. Returns decoded codes like "P0301"; an empty
     * (non-null) list means the ECU responded with no stored codes, which is a valid result.
     */
    fun readStandardDTCs(): List<String>? {
        return try {
            bluetoothManager.setHeader("Auto")
            val fullResponse = bluetoothManager.sendCommand("03") ?: return null
            if (fullResponse.contains("UNABLE TO CONNECT") || fullResponse.contains("BUS ERROR")) {
                Timber.w("DTC read failed: $fullResponse")
                return null
            }
            val cleanResponse = fullResponse.replace("\\s+".toRegex(), "").uppercase()
            val dataBytes = if (cleanResponse.startsWith("43")) cleanResponse.substring(2) else cleanResponse
            decodeDTCs(dataBytes)
        } catch (e: Exception) {
            Timber.e(e, "Error reading DTCs")
            null
        }
    }

    /**
     * Clears stored DTCs and turns off the MIL via standard SAE J1979 Mode 04. This is a WRITE
     * to the vehicle - callers must get explicit user confirmation before calling this, since it
     * also resets the readiness monitors. Returns true only if the adapter's response confirms
     * the clear (echoes "44"); false covers both a real failure and "adapter didn't confirm."
     */
    fun clearStandardDTCs(): Boolean {
        return try {
            bluetoothManager.setHeader("Auto")
            val response = bluetoothManager.sendCommand("04") ?: return false
            val clean = response.replace("\\s+".toRegex(), "").uppercase()
            clean.contains("44") && !clean.contains("NODATA") && !clean.contains("ERROR")
        } catch (e: Exception) {
            Timber.e(e, "Error clearing DTCs")
            false
        }
    }

    /**
     * GM enhanced DTC read via UDS-style Service 0x19 - UNVERIFIED on this VIN. GM's enhanced
     * bus sometimes exposes additional manufacturer-specific codes this way that Mode 03 won't
     * show, but the exact sub-function/response format needs confirming against a real scan
     * before this is trusted. Returns the raw adapter response, undecoded.
     */
    fun readEnhancedDTCsRaw(): String? {
        bluetoothManager.setHeader("Auto")
        return bluetoothManager.sendCommand("1902")
    }

    /**
     * GM enhanced DTC clear via UDS-style Service 0x14 - UNVERIFIED on this VIN, same caveat as
     * [readEnhancedDTCsRaw]. This is a WRITE - confirm with the user before calling it.
     */
    fun clearEnhancedDTCsRaw(): String? {
        bluetoothManager.setHeader("Auto")
        return bluetoothManager.sendCommand("14FF00")
    }

    /**
     * Pure response-parsing formulas. These don't need a Bluetooth connection, so they live
     * on the companion object and PIDDatabase.kt references them directly (e.g.
     * OBD2Protocol.parseRPM) when building each PIDParameter's `parse` lambda.
     */
    companion object {

        /** First data byte (A) as an unsigned int, or null if the response is too short/invalid. */
        fun byte(response: String, index: Int = 0): Int? {
            val start = index * 2
            if (response.length < start + 2) return null
            return response.substring(start, start + 2).toIntOrNull(16)
        }

        /** Two consecutive data bytes (A*256 + B) as an unsigned int. */
        fun word(response: String, startIndex: Int = 0): Int? {
            val a = byte(response, startIndex) ?: return null
            val b = byte(response, startIndex + 1) ?: return null
            return (a * 256) + b
        }

        /**
         * Parse RPM from OBD2 response
         * PID 010C: ((A*256)+B)/4
         */
        fun parseRPM(response: String): Double? {
            return try {
                if (response.length < 4) return null
                val a = response.substring(0, 2).toInt(16)
                val b = response.substring(2, 4).toInt(16)
                ((a * 256 + b) / 4.0)
            } catch (e: Exception) {
                Timber.e(e, "Error parsing RPM")
                null
            }
        }

        /**
         * Parse Coolant Temperature from OBD2 response
         * PID 0105: A-40
         */
        fun parseCoolantTemp(response: String): Double? {
            return try {
                if (response.length < 2) return null
                val a = response.substring(0, 2).toInt(16)
                (a - 40).toDouble()
            } catch (e: Exception) {
                Timber.e(e, "Error parsing coolant temp")
                null
            }
        }

        /**
         * Parse Intake Air Temperature
         * PID 010F: A-40
         */
        fun parseIntakeAirTemp(response: String): Double? {
            return try {
                if (response.length < 2) return null
                val a = response.substring(0, 2).toInt(16)
                (a - 40).toDouble()
            } catch (e: Exception) {
                Timber.e(e, "Error parsing intake air temp")
                null
            }
        }

        /**
         * Parse Engine Load (Absolute)
         * PID 0143: ((A*256)+B)*100/65536
         */
        fun parseEngineLoad(response: String): Double? {
            return try {
                if (response.length < 4) return null
                val a = response.substring(0, 2).toInt(16)
                val b = response.substring(2, 4).toInt(16)
                ((a * 256 + b) * 100.0 / 65536.0)
            } catch (e: Exception) {
                Timber.e(e, "Error parsing engine load")
                null
            }
        }

        /**
         * Parse Calculated Load Value (single-byte, distinct from Absolute Load above)
         * PID 0104: A*100/255
         */
        fun parseCalculatedLoad(response: String): Double? {
            return try {
                if (response.length < 2) return null
                val a = response.substring(0, 2).toInt(16)
                (a * 100.0 / 255.0)
            } catch (e: Exception) {
                Timber.e(e, "Error parsing calculated load")
                null
            }
        }

        /**
         * Parse MAP Sensor - scaled for the installed 3 Bar sensor (300 kPa max).
         * The factory MAP sensor is only 1 Bar (255 kPa max per the standard OBD2 formula);
         * this build runs an aftermarket 3 Bar sensor, so the standard formula must NOT be used
         * as-is. Update this scaling any time the physical MAP sensor on the car changes.
         * PID 010B: (A/255)*300
         */
        fun parseMAP(response: String): Double? {
            return try {
                if (response.length < 2) return null
                val a = response.substring(0, 2).toInt(16)
                (a / 255.0) * 300.0
            } catch (e: Exception) {
                Timber.e(e, "Error parsing MAP")
                null
            }
        }

        /**
         * Parse Throttle Position
         * PID 0111: A*100/255 (%)
         */
        fun parseThrottlePosition(response: String): Double? {
            return try {
                if (response.length < 2) return null
                val a = response.substring(0, 2).toInt(16)
                (a * 100.0 / 255.0)
            } catch (e: Exception) {
                Timber.e(e, "Error parsing throttle position")
                null
            }
        }

        /**
         * Parse MAF Air Flow Rate
         * PID 0110: ((A*256)+B)/100 (g/s)
         */
        fun parseMAF(response: String): Double? {
            return try {
                if (response.length < 4) return null
                val a = response.substring(0, 2).toInt(16)
                val b = response.substring(2, 4).toInt(16)
                ((a * 256 + b) / 100.0)
            } catch (e: Exception) {
                Timber.e(e, "Error parsing MAF")
                null
            }
        }

        /**
         * Parse Engine Oil Temperature
         * PID 015C: A-40 (°C)
         */
        fun parseOilTemp(response: String): Double? {
            return try {
                if (response.length < 2) return null
                val a = response.substring(0, 2).toInt(16)
                (a - 40).toDouble()
            } catch (e: Exception) {
                Timber.e(e, "Error parsing oil temp")
                null
            }
        }

        /**
         * Parse Ambient Air Temperature
         * PID 0146: A-40 (°C)
         */
        fun parseAmbientTemp(response: String): Double? {
            return try {
                if (response.length < 2) return null
                val a = response.substring(0, 2).toInt(16)
                (a - 40).toDouble()
            } catch (e: Exception) {
                Timber.e(e, "Error parsing ambient temp")
                null
            }
        }

        /**
         * Parse Absolute Barometric Pressure
         * PID 0133: A (kPa)
         */
        fun parseBaroPressure(response: String): Double? {
            return try {
                if (response.length < 2) return null
                response.substring(0, 2).toInt(16).toDouble()
            } catch (e: Exception) {
                Timber.e(e, "Error parsing barometric pressure")
                null
            }
        }

        /**
         * Parse Fuel Tank Level
         * PID 012F: A*100/255 (%)
         */
        fun parseFuelLevel(response: String): Double? {
            return try {
                if (response.length < 2) return null
                val a = response.substring(0, 2).toInt(16)
                (a * 100.0 / 255.0)
            } catch (e: Exception) {
                Timber.e(e, "Error parsing fuel level")
                null
            }
        }

        /**
         * Parse Fuel Pressure (Gauge)
         * PID 010A: A*3 (kPa, for gauge fuel pressure)
         */
        fun parseFuelPressure(response: String): Double? {
            return try {
                if (response.length < 2) return null
                val a = response.substring(0, 2).toInt(16)
                (a * 3).toDouble()
            } catch (e: Exception) {
                Timber.e(e, "Error parsing fuel pressure")
                null
            }
        }

        /**
         * Parse Ignition Timing Advance
         * PID 010E: (A/2)-64 (degrees BTDC)
         */
        fun parseIgnitionTiming(response: String): Double? {
            return try {
                if (response.length < 2) return null
                val a = response.substring(0, 2).toInt(16)
                (a / 2.0) - 64.0
            } catch (e: Exception) {
                Timber.e(e, "Error parsing ignition timing")
                null
            }
        }

        /**
         * Parse Oxygen Sensor Voltage
         * PIDs 0114, 0115, 0116, 0117: A*8/65535 (V)
         */
        fun parseO2Voltage(response: String): Double? {
            return try {
                if (response.length < 2) return null
                val a = response.substring(0, 2).toInt(16)
                (a * 8.0 / 65535.0)
            } catch (e: Exception) {
                Timber.e(e, "Error parsing O2 voltage")
                null
            }
        }

        /**
         * Parse Short Term Fuel Trim
         * PID 0106, 0108: (A-128)*100/128 (%)
         */
        fun parseShortFuelTrim(response: String): Double? {
            return try {
                if (response.length < 2) return null
                val a = response.substring(0, 2).toInt(16)
                ((a - 128) * 100.0 / 128.0)
            } catch (e: Exception) {
                Timber.e(e, "Error parsing short fuel trim")
                null
            }
        }

        /**
         * Parse Long Term Fuel Trim
         * PID 0107, 0109: (A-128)*100/128 (%)
         */
        fun parseLongFuelTrim(response: String): Double? {
            return try {
                if (response.length < 2) return null
                val a = response.substring(0, 2).toInt(16)
                ((a - 128) * 100.0 / 128.0)
            } catch (e: Exception) {
                Timber.e(e, "Error parsing long fuel trim")
                null
            }
        }

        /**
         * Parse Vehicle Speed
         * PID 010D: A (km/h)
         */
        fun parseVehicleSpeed(response: String): Double? {
            return try {
                if (response.length < 2) return null
                val a = response.substring(0, 2).toInt(16)
                a.toDouble()
            } catch (e: Exception) {
                Timber.e(e, "Error parsing vehicle speed")
                null
            }
        }

        /**
         * Parse Transmission Fluid Temperature (placeholder PID, unverified - see PIDDatabase)
         * Custom scaling: A-40 (degrees C)
         */
        fun parseTransmissionTemp(response: String): Double? {
            return try {
                if (response.length < 2) return null
                val a = response.substring(0, 2).toInt(16)
                (a - 40).toDouble()
            } catch (e: Exception) {
                Timber.e(e, "Error parsing transmission temp")
                null
            }
        }

        /** Raw hex byte value with no scaling - used for placeholder/unverified PIDs. */
        fun parseRawByte(response: String): Double? = byte(response)?.toDouble()

        /**
         * Decodes raw Mode 03 DTC data bytes into standard 5-character codes (e.g. "P0301").
         * Each code is 2 bytes: the top 2 bits of the first byte pick the P/C/B/U prefix, the
         * next 2 bits are the second digit, the low nibble is the third digit (hex), and the
         * second byte is the last two digits (hex). A "0000" pair is padding, not a real code.
         */
        fun decodeDTCs(dataBytes: String): List<String> {
            val codes = mutableListOf<String>()
            var i = 0
            while (i + 4 <= dataBytes.length) {
                val pair = dataBytes.substring(i, i + 4)
                i += 4
                if (pair == "0000") continue

                val byte1 = pair.substring(0, 2).toIntOrNull(16) ?: continue
                val byte2 = pair.substring(2, 4)

                val prefix = when ((byte1 shr 6) and 0x03) {
                    0 -> "P"
                    1 -> "C"
                    2 -> "B"
                    else -> "U"
                }
                val secondDigit = (byte1 shr 4) and 0x03
                val thirdDigit = (byte1 and 0x0F).toString(16).uppercase()

                codes.add("$prefix$secondDigit$thirdDigit$byte2")
            }
            return codes
        }
    }
}
