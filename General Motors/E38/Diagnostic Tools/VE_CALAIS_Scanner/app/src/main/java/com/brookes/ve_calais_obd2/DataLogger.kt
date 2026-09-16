package com.brookes.ve_calais_obd2

import android.content.Context
import android.os.Environment
import com.google.gson.Gson
import com.google.gson.GsonBuilder
import timber.log.Timber
import java.io.File
import java.io.FileWriter
import java.text.SimpleDateFormat
import java.util.*

data class LogEntry(
    val timestamp: Long,
    val data: Map<String, Any?>
)

data class SessionLog(
    val sessionId: String,
    val startTime: Long,
    var endTime: Long = 0,
    val owner: String,
    val vehicle: String,
    val engineModel: String,
    val ecuId: String,
    val entries: MutableList<LogEntry> = mutableListOf()
)

class DataLogger(private val context: Context) {

    private val logsDirectory: File by lazy {
        val dir = File(context.getExternalFilesDir(Environment.DIRECTORY_DOCUMENTS), "VECalaisLogs")
        dir.mkdirs()
        dir
    }

    private val gson: Gson = GsonBuilder()
        .setPrettyPrinting()
        .setDateFormat("yyyy-MM-dd HH:mm:ss")
        .create()

    private val dateFormat = SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.US)
    private val filenameDateFormat = SimpleDateFormat("yyyyMMdd_HHmmss", Locale.US)

    fun createNewSession(
        owner: String,
        vehicle: String,
        engineModel: String,
        ecuId: String
    ): SessionLog {
        return SessionLog(
            sessionId = UUID.randomUUID().toString(),
            startTime = System.currentTimeMillis(),
            owner = owner,
            vehicle = vehicle,
            engineModel = engineModel,
            ecuId = ecuId
        )
    }

    /**
     * Add data entry to session
     */
    fun addEntry(session: SessionLog, data: Map<String, Any?>) {
        session.entries.add(
            LogEntry(
                timestamp = System.currentTimeMillis(),
                data = data
            )
        )
    }

    /**
     * Export session as CSV
     */
    fun exportAsCSV(session: SessionLog): Boolean {
        return try {
            val filename = "VE_Calais_${filenameDateFormat.format(Date(session.startTime))}.csv"
            val file = File(logsDirectory, filename)

            FileWriter(file).use { writer ->
                // Header with session info
                writer.append("VE Calais L77 OBD2 Data Log\n")
                writer.append("Owner,${session.owner}\n")
                writer.append("Vehicle,${session.vehicle}\n")
                writer.append("Engine,${session.engineModel}\n")
                writer.append("ECU,${session.ecuId}\n")
                writer.append("Session ID,${session.sessionId}\n")
                writer.append("Start Time,${dateFormat.format(Date(session.startTime))}\n")
                writer.append("Duration Seconds,${(session.endTime - session.startTime) / 1000}\n")
                writer.append("\n")

                // Column headers
                if (session.entries.isNotEmpty()) {
                    val headers = mutableSetOf("Timestamp")
                    headers.addAll(session.entries[0].data.keys)
                    writer.append(headers.joinToString(","))
                    writer.append("\n")

                    // Data rows
                    session.entries.forEach { entry ->
                        val values = mutableListOf(dateFormat.format(Date(entry.timestamp)))
                        headers.drop(1).forEach { header ->
                            val value = entry.data[header]?.toString() ?: ""
                            values.add(escapeCSV(value))
                        }
                        writer.append(values.joinToString(","))
                        writer.append("\n")
                    }
                }
            }

            Timber.i("Session exported to CSV: $filename")
            true
        } catch (e: Exception) {
            Timber.e(e, "Failed to export session as CSV")
            false
        }
    }

    /**
     * Export session as JSON
     */
    fun exportAsJSON(session: SessionLog): Boolean {
        return try {
            val filename = "VE_Calais_${filenameDateFormat.format(Date(session.startTime))}.json"
            val file = File(logsDirectory, filename)

            FileWriter(file).use { writer ->
                gson.toJson(session, writer)
            }

            Timber.i("Session exported to JSON: $filename")
            true
        } catch (e: Exception) {
            Timber.e(e, "Failed to export session as JSON")
            false
        }
    }

    /**
     * Export session as PDF Report
     */
    fun exportAsPDFReport(session: SessionLog): Boolean {
        return try {
            val filename = "VE_Calais_${filenameDateFormat.format(Date(session.startTime))}_Report.txt"
            val file = File(logsDirectory, filename)

            FileWriter(file).use { writer ->
                writer.append("═".repeat(80) + "\n")
                writer.append("VE CALAIS L77 OBD2 DATA SESSION REPORT\n")
                writer.append("═".repeat(80) + "\n\n")

                writer.append("VEHICLE INFORMATION\n")
                writer.append("─".repeat(80) + "\n")
                writer.append("Owner: ${session.owner}\n")
                writer.append("Vehicle: ${session.vehicle}\n")
                writer.append("Engine: ${session.engineModel}\n")
                writer.append("ECU: ${session.ecuId}\n")
                writer.append("Session ID: ${session.sessionId}\n\n")

                writer.append("SESSION DETAILS\n")
                writer.append("─".repeat(80) + "\n")
                writer.append("Start Time: ${dateFormat.format(Date(session.startTime))}\n")
                writer.append("End Time: ${dateFormat.format(Date(session.endTime))}\n")
                val durationSeconds = (session.endTime - session.startTime) / 1000
                writer.append("Duration: $durationSeconds seconds\n")
                writer.append("Data Points: ${session.entries.size}\n\n")

                if (session.entries.isNotEmpty()) {
                    writer.append("DATA SUMMARY\n")
                    writer.append("─".repeat(80) + "\n")

                    // Calculate statistics for numeric values
                    val allKeys = session.entries.flatMap { it.data.keys }.toSet()
                    allKeys.forEach { key ->
                        val values = session.entries.mapNotNull {
                            (it.data[key] as? Number)?.toDouble()
                        }
                        if (values.isNotEmpty()) {
                            val min = values.minOrNull() ?: 0.0
                            val max = values.maxOrNull() ?: 0.0
                            val avg = values.average()
                            writer.append("$key:\n")
                            writer.append("  Min: %.2f | Max: %.2f | Avg: %.2f\n".format(min, max, avg))
                        }
                    }

                    writer.append("\n")
                    writer.append("RAW DATA\n")
                    writer.append("─".repeat(80) + "\n")
                    session.entries.forEach { entry ->
                        writer.append("${dateFormat.format(Date(entry.timestamp))}: ")
                        writer.append(entry.data.entries.joinToString(", ") { "${it.key}=${it.value}" })
                        writer.append("\n")
                    }
                }

                writer.append("\n")
                writer.append("═".repeat(80) + "\n")
                writer.append("Generated: ${dateFormat.format(Date())}\n")
                writer.append("VE Calais OBD2 Reader v1.0.0\n")
            }

            Timber.i("Session exported to PDF Report: $filename")
            true
        } catch (e: Exception) {
            Timber.e(e, "Failed to export session as PDF report")
            false
        }
    }

    /**
     * Get all saved sessions
     */
    fun getAllSessions(): List<File> {
        return logsDirectory.listFiles()?.toList() ?: emptyList()
    }

    /**
     * Delete a session
     */
    fun deleteSession(file: File): Boolean {
        return try {
            file.delete().also {
                if (it) Timber.i("Session deleted: ${file.name}")
            }
        } catch (e: Exception) {
            Timber.e(e, "Failed to delete session")
            false
        }
    }

    /**
     * Get logs directory path for file access
     */
    fun getLogsDirectoryPath(): String {
        return logsDirectory.absolutePath
    }

    /**
     * Export PID Scanner results as CSV, in the same column layout as did_sweeper.py's
     * SCAN_RESULTS_verified_dids.csv so results from either tool are directly comparable.
     */
    fun exportScanResults(records: List<ScanRecord>): Boolean {
        return try {
            val filename = "pid_scan_${filenameDateFormat.format(Date())}.csv"
            val file = File(logsDirectory, filename)

            FileWriter(file).use { writer ->
                writer.append("header,did,mode_and_pid,status,detail,module\n")
                records.forEach { r ->
                    writer.append("${r.header},${r.did},0x22${r.did.lowercase()},${r.status},${escapeCSV(r.detail)},${escapeCSV(r.module)}\n")
                }
            }

            Timber.i("Scan results exported: $filename")
            true
        } catch (e: Exception) {
            Timber.e(e, "Failed to export scan results")
            false
        }
    }

    /**
     * Export DTC read results as a date-stamped CSV, so a code read is on record even if it
     * gets cleared straight after (e.g. before/after a repair).
     */
    fun exportDtcResults(codes: List<String>): Boolean {
        return try {
            val filename = "dtc_read_${filenameDateFormat.format(Date())}.csv"
            val file = File(logsDirectory, filename)

            FileWriter(file).use { writer ->
                writer.append("code,read_at\n")
                val timestamp = Date().toString()
                if (codes.isEmpty()) {
                    writer.append("NONE,$timestamp\n")
                } else {
                    codes.forEach { code -> writer.append("$code,$timestamp\n") }
                }
            }

            Timber.i("DTC results exported: $filename")
            true
        } catch (e: Exception) {
            Timber.e(e, "Failed to export DTC results")
            false
        }
    }

    /**
     * Escape special characters in CSV values
     */
    private fun escapeCSV(value: String): String {
        return if (value.contains(",") || value.contains("\"") || value.contains("\n")) {
            "\"" + value.replace("\"", "\"\"") + "\""
        } else {
            value
        }
    }
}
