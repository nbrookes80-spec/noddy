package com.brookes.ve_calais_obd2

data class ScanBlock(val header: String, val highBytes: List<Int>, val label: String)

data class ScanRecord(
    val header: String,
    val did: String,
    val status: String,
    val detail: String,
    val module: String
)

/**
 * Mode 22 DID sweeper - ports the logic from did_sweeper.py (the companion Python tool that
 * drove a manual TorqueScan Telnet sweep) so the same targeted, per-module sweep can run
 * directly from the phone over the app's own Bluetooth connection - no laptop or Telnet
 * bridge needed. Response classification matches the Python script exactly (same parser,
 * same negative-response-code table) so results are directly comparable to a prior run.
 */
object PidScanner {

    // Blocks GM actually populates on this VIN, from the DID scan protocol doc.
    val DEFAULT_PLAN = listOf(
        ScanBlock("7E2", listOf(0x19, 0x1A, 0x00, 0x3D, 0x10, 0x11), "T43 TCM - trans data"),
        ScanBlock("7E0", listOf(0x11, 0x12, 0x14, 0x15, 0x16, 0x20, 0x22, 0x0C), "E38 ECM - engine data"),
        ScanBlock("7E3", listOf(0x11, 0x14), "FPCM - fuel pump")
    )

    private val NRC_MEANINGS = mapOf(
        "11" to "serviceNotSupported",
        "12" to "subFunctionNotSupported",
        "31" to "requestOutOfRange",
        "22" to "conditionsNotCorrect",
        "33" to "securityAccessDenied",
        "78" to "responsePending"
    )

    /** Classifies a raw ELM327 response to a "22<did>" request. Mirrors did_sweeper.py::classify. */
    fun classify(did: String, rawResponse: String): Pair<String, String> {
        val h = normalize(rawResponse)
        val d = did.uppercase()
        val marker = "62$d"
        if (h.contains(marker)) {
            val i = h.indexOf(marker) + marker.length
            return "SUPPORTED" to h.substring(i, minOf(i + 16, h.length))
        }
        for ((nrc, meaning) in NRC_MEANINGS) {
            if (h.contains("7F22$nrc")) return "REJECTED_$nrc" to meaning
        }
        return when {
            h.contains("NODATA") -> "NO_DATA" to ""
            h.contains("CANERROR") -> "CAN_ERROR" to ""
            h.contains("BUSINIT") || h.contains("BUSERROR") -> "BUS_ERROR" to ""
            h.isBlank() || h == "?" -> "NO_REPLY" to ""
            else -> "UNKNOWN" to h.take(40)
        }
    }

    private fun normalize(response: String): String {
        return response.replace(">", " ")
            .replace(Regex("[\\r\\n]+"), " ")
            .replace(Regex("\\s+"), "")
            .uppercase()
    }

    fun totalRequests(plan: List<ScanBlock>): Int = plan.sumOf { it.highBytes.size } * 256
}
