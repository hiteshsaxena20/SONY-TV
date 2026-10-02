package com.sonytv.remote.service

import android.app.Service
import android.content.Intent
import android.os.IBinder

class AgentService : Service() {
    
    override fun onBind(intent: Intent?): IBinder? = null
    
    override fun onCreate() {
        super.onCreate()
        // 1. Start foreground service
        // 2. Start Ktor WebSocket server for LAN
        // 3. Register mDNS to broadcast presence
    }
    
    override fun onDestroy() {
        super.onDestroy()
        // Cleanup
    }
}
