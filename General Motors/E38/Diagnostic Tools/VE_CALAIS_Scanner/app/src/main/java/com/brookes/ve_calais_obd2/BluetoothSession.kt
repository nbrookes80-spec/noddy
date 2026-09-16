package com.brookes.ve_calais_obd2

import android.content.Context

/**
 * One BluetoothManager instance for the whole app's lifetime, so the Live Data dashboard, PID
 * Scanner, and Sniffer screens all share the same physical connection to the OBD2 adapter
 * instead of each opening (and fighting over) their own socket.
 */
object BluetoothSession {

    @Volatile
    private var manager: BluetoothManager? = null

    fun get(context: Context): BluetoothManager {
        return manager ?: synchronized(this) {
            manager ?: BluetoothManager(context.applicationContext).also { manager = it }
        }
    }
}
