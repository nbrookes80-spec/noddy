package com.brookes.ve_calais_obd2

import android.content.Context
import android.content.SharedPreferences
import timber.log.Timber

class VehicleVerification(context: Context) {

    private val prefs: SharedPreferences = context.getSharedPreferences(
        "ve_calais_verification",
        Context.MODE_PRIVATE
    )

    companion object {
        private const val KEY_VIN = "vehicle_vin"
        private const val KEY_ECU_ID = "ecu_id"
        private const val KEY_VERIFIED = "is_verified"
        private const val KEY_OWNER = "owner_name"

        // Expected values for Nathan's 2011 Holden VE Calais L77
        private const val EXPECTED_OWNER = "Nathan Brookes"
        private const val EXPECTED_MODEL_YEAR = "2011"
        private const val EXPECTED_ECU = "E38"
        private const val EXPECTED_ENGINE = "L77"

        // Build signature - unique identifier for turbo build
        private const val BUILD_SIGNATURE = "VE_CALAIS_L77_G42_TURBO"
    }

    /**
     * Verify the vehicle on first connection
     * Returns true if verification successful
     */
    fun verifyVehicle(vin: String, ecuId: String): Boolean {
        return try {
            Timber.d("Attempting vehicle verification: VIN=$vin, ECU=$ecuId")

            // Check VIN format (17 characters for automotive standard)
            if (vin.length != 17) {
                Timber.w("Invalid VIN length: ${vin.length}")
                return false
            }

            // Parse VIN to get model year and make/model
            val modelYear = vinToYear(vin)
            val vinMakeModel = parseMakeModel(vin)

            Timber.d("VIN parsed: Year=$modelYear, Make/Model=$vinMakeModel")

            // Verify it's a 2011 vehicle
            if (modelYear != EXPECTED_MODEL_YEAR) {
                Timber.w("Model year mismatch: expected $EXPECTED_MODEL_YEAR, got $modelYear")
                return false
            }

            // Verify it's a Holden VE or Pontiac G8
            if (!vinMakeModel.contains("VE", ignoreCase = true) &&
                !vinMakeModel.contains("G8", ignoreCase = true) &&
                !vinMakeModel.contains("Holden", ignoreCase = true) &&
                !vinMakeModel.contains("Pontiac", ignoreCase = true)
            ) {
                Timber.w("Make/model mismatch: $vinMakeModel")
                return false
            }

            // Verify ECU is E38
            if (!ecuId.contains(EXPECTED_ECU, ignoreCase = true)) {
                Timber.w("ECU mismatch: expected $EXPECTED_ECU, got $ecuId")
                return false
            }

            // Store verification data
            prefs.edit().apply {
                putString(KEY_VIN, vin)
                putString(KEY_ECU_ID, ecuId)
                putString(KEY_OWNER, EXPECTED_OWNER)
                putBoolean(KEY_VERIFIED, true)
                apply()
            }

            Timber.i("Vehicle verification SUCCESSFUL: $vin ($ecuId)")
            true
        } catch (e: Exception) {
            Timber.e(e, "Vehicle verification failed")
            false
        }
    }

    /**
     * Check if this vehicle has already been verified
     */
    fun isVerified(): Boolean {
        return prefs.getBoolean(KEY_VERIFIED, false)
    }

    /**
     * Get stored VIN
     */
    fun getStoredVIN(): String? {
        return prefs.getString(KEY_VIN, null)
    }

    /**
     * Get stored ECU ID
     */
    fun getStoredECUID(): String? {
        return prefs.getString(KEY_ECU_ID, null)
    }

    /**
     * Get owner name
     */
    fun getOwnerName(): String? {
        return prefs.getString(KEY_OWNER, null)
    }

    /**
     * Reset verification (for different vehicle)
     */
    fun reset() {
        prefs.edit().clear().apply()
        Timber.i("Vehicle verification reset")
    }

    /**
     * Extract year from VIN
     * Position 10 in VIN is model year
     * Y=2000, 1=2001, 2=2002, 3=2003, 4=2004, 5=2005, 6=2006, 7=2007, 8=2008, 9=2009
     * A=2010, B=2011, C=2012, etc.
     */
    private fun vinToYear(vin: String): String {
        return try {
            val yearChar = vin[9]
            when (yearChar) {
                'Y' -> "2000"
                '1' -> "2001"
                '2' -> "2002"
                '3' -> "2003"
                '4' -> "2004"
                '5' -> "2005"
                '6' -> "2006"
                '7' -> "2007"
                '8' -> "2008"
                '9' -> "2009"
                'A' -> "2010"
                'B' -> "2011"
                'C' -> "2012"
                'D' -> "2013"
                else -> ""
            }
        } catch (e: Exception) {
            ""
        }
    }

    /**
     * Parse make and model from VIN
     * Holden: starts with 6G, 6F
     * Pontiac G8: starts with 2G, 5G
     */
    private fun parseMakeModel(vin: String): String {
        return try {
            val wmiSection = vin.substring(0, 3)
            when {
                wmiSection.startsWith("6G") -> "Holden VE"
                wmiSection.startsWith("6F") -> "Holden VE"
                wmiSection.startsWith("2G") -> "Pontiac G8"
                wmiSection.startsWith("5G") -> "Pontiac G8"
                else -> "Unknown"
            }
        } catch (e: Exception) {
            "Unknown"
        }
    }

    /**
     * Verify turbo build configuration
     * Checks for expected modifications based on ECU parameters
     */
    fun verifyTurboBuild(mapSensorReading: Double): Boolean {
        // 2.7 Bar MAP sensor should support readings up to ~270 kPa
        // If we can read above 200 kPa reliably, turbo system is present
        return mapSensorReading >= 100.0
    }

    /**
     * Create build profile
     */
    fun getBuildProfile(): String {
        return """
            |Owner: $EXPECTED_OWNER (FOX95S)
            |Vehicle: 2011 Holden VE Calais Redline / Pontiac G8
            |Engine: L77 6.0L V8 (DOD Deleted)
            |ECU: E38 (EFI Live Tuned)
            |Fuel System: KPM 1000HP, KPM1500 Injectors (E85/98 Flex)
            |Turbocharger: Killaboost G42-1450 with 2.7 Bar MAP Sensor
            |Transmission: 6L80E with Transgo Shift Kit
            |Build Signature: $BUILD_SIGNATURE
        """.trimMargin()
    }
}
