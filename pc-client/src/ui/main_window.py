from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget, QLabel
from PySide6.QtCore import Qt
from src.ui.remote_panel import RemotePanel
from src.network.websocket_client import WebSocketClient
from src.network.discovery import DiscoveryManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎮 SONY TV Remote")
        self.setMinimumSize(400, 600)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        
        # Status Bar / Header
        self.status_label = QLabel("📺 Searching for TV on LAN...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; margin: 10px; color: gray;")
        self.layout.addWidget(self.status_label)
        
        # Tabs
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)
        
        # Remote Tab (Phase 1)
        self.remote_panel = RemotePanel()
        self.tabs.addTab(self.remote_panel, "Remote")
        
        # Placeholders for future phases
        self.tabs.addTab(QLabel("Screen Viewing (Phase 3)"), "Screen")
        self.tabs.addTab(QLabel("Keyboard (Phase 4)"), "Keyboard")
        self.tabs.addTab(QLabel("Apps (Phase 4)"), "Apps")

        # Network setup
        self.ws_client = WebSocketClient()
        self.ws_client.connected.connect(self.on_connected)
        self.ws_client.disconnected.connect(self.on_disconnected)
        self.ws_client.error_occurred.connect(self.on_error)
        
        self.discovery = DiscoveryManager()
        self.discovery.tv_found.connect(self.on_tv_found)
        self.discovery.start()

        # Connect UI signals
        self.remote_panel.command_requested.connect(self.handle_command)

    def on_tv_found(self, name, ip, port):
        self.status_label.setText(f"📺 Found: {name} - Connecting...")
        self.ws_client.connect_to_url(f"ws://{ip}:{port}")
        self.discovery.stop()

    def on_connected(self):
        self.status_label.setText("📺 TV: Connected ●")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; margin: 10px; color: green;")

    def on_disconnected(self):
        self.status_label.setText("📺 TV: Offline ●")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; margin: 10px; color: red;")

    def on_error(self, error):
        self.status_label.setText(f"📺 Connection Error: {error}")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; margin: 10px; color: red;")

    def handle_command(self, action):
        # Map some commands to categories
        category = "remote_control"
        if action.startswith("KEY_VOLUME") or action == "KEY_MUTE":
            category = "volume"
        elif action in ("KEY_POWER", "KEY_SLEEP", "KEY_WAKEUP"):
            category = "power"
        elif action.startswith("KEY_MEDIA"):
            category = "media"
            
        self.ws_client.send_command(category, action)

    def closeEvent(self, event):
        self.ws_client.disconnect()
        self.discovery.stop()
        super().closeEvent(event)
