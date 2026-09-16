package com.brookes.ve_calais_obd2

import android.content.Context
import java.util.UUID

/**
 * Owns the current data-logging session so it starts the moment the app connects to the
 * adapter (not just when "Start Monitoring" is tapped) and survives navigating between
 * screens. Auto-saves (CSV + JSON, date-stamped filenames) whenever a session ends, so nothing
 * has to be manually exported to keep a record of a connection.
 */
object SessionManager {

    private var currentSession: SessionLog? = null

    fun current(): SessionLog? = currentSession

    /** Starts a new session, auto-saving and closing out any previous one first. */
    fun startNewSession(context: Context): SessionLog {
        endCurrentSession(context)
        val session = SessionLog(
            sessionId = UUID.randomUUID().toString(),
            startTime = System.currentTimeMillis(),
            owner = "Nathan Brookes",
            vehicle = "2011 Holden VE Calais Redline",
            engineModel = "L77 6.0L V8",
            ecuId = "E38"
        )
        currentSession = session
        return session
    }

    fun getOrStartSession(context: Context): SessionLog {
        return currentSession ?: startNewSession(context)
    }

    /** Ends and auto-saves the current session (CSV + JSON), if one is running. */
    fun endCurrentSession(context: Context): SessionLog? {
        val session = currentSession ?: return null
        session.endTime = System.currentTimeMillis()
        val logger = DataLogger(context)
        logger.exportAsCSV(session)
        logger.exportAsJSON(session)
        currentSession = null
        return session
    }
}
