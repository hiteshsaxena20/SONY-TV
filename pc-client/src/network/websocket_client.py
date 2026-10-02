import asyncio
import json
import uuid
import time
from PySide6.QtCore import QObject, Signal, QThread
import websockets

class WebSocketWorker(QObject):
    connected = Signal()
    disconnected = Signal()
    message_received = Signal(dict)
    error_occurred = Signal(str)

    def __init__(self):
        super().__init__()
        self.url = ""
        self.running = False
        self.websocket = None
        self.loop = None

    def start_connection(self, url):
        self.url = url
        self.running = True
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._connect_and_listen())

    async def _connect_and_listen(self):
        try:
            async with websockets.connect(self.url) as websocket:
                self.websocket = websocket
                self.connected.emit()
                while self.running:
                    try:
                        # Use wait_for to periodically check if running is False
                        message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                        data = json.loads(message)
                        self.message_received.emit(data)
                    except asyncio.TimeoutError:
                        continue
                    except websockets.exceptions.ConnectionClosed:
                        break
        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            self.websocket = None
            self.disconnected.emit()

    def send_command(self, category, action, params=None):
        if not self.websocket or not self.running:
            return

        cmd = {
            "version": 1,
            "type": "COMMAND",
            "id": str(uuid.uuid4()),
            "timestamp": int(time.time() * 1000),
            "device_id": "tv-living-room-abc123", # Placeholder
            "command": {
                "category": category,
                "action": action,
                "params": params or {}
            }
        }
        
        asyncio.run_coroutine_threadsafe(
            self.websocket.send(json.dumps(cmd)),
            self.loop
        )

    def stop(self):
        self.running = False
        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)

class WebSocketClient(QObject):
    connected = Signal()
    disconnected = Signal()
    message_received = Signal(dict)
    error_occurred = Signal(str)

    def __init__(self):
        super().__init__()
        self.worker = WebSocketWorker()
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        
        self.worker.connected.connect(self.connected)
        self.worker.disconnected.connect(self.disconnected)
        self.worker.message_received.connect(self.message_received)
        self.worker.error_occurred.connect(self.error_occurred)

    def connect_to_url(self, url):
        self.thread.started.connect(lambda: self.worker.start_connection(url))
        self.thread.start()

    def send_command(self, category, action, params=None):
        self.worker.send_command(category, action, params)

    def disconnect(self):
        self.worker.stop()
        self.thread.quit()
        self.thread.wait()
