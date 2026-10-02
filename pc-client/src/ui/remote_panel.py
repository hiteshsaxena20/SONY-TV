from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout
from PySide6.QtCore import Qt, Signal

class RemotePanel(QWidget):
    # Signal to emit when a button is pressed, sending the command name
    command_requested = Signal(str)

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        
        self.setup_dpad()
        self.setup_control_bar()
        self.setup_volume_bar()
        self.setup_media_controls()
        self.setup_power_controls()
        
        self.layout.addStretch()

    def create_btn(self, text, command, min_height=40):
        btn = QPushButton(text)
        btn.setMinimumHeight(min_height)
        btn.clicked.connect(lambda: self.command_requested.emit(command))
        return btn

    def setup_dpad(self):
        grid = QGridLayout()
        
        btn_up = self.create_btn("▲", "KEY_DPAD_UP", 60)
        btn_down = self.create_btn("▼", "KEY_DPAD_DOWN", 60)
        btn_left = self.create_btn("◄", "KEY_DPAD_LEFT", 60)
        btn_right = self.create_btn("►", "KEY_DPAD_RIGHT", 60)
        btn_ok = self.create_btn("OK", "KEY_DPAD_CENTER", 60)
        
        grid.addWidget(btn_up, 0, 1)
        grid.addWidget(btn_left, 1, 0)
        grid.addWidget(btn_ok, 1, 1)
        grid.addWidget(btn_right, 1, 2)
        grid.addWidget(btn_down, 2, 1)
        
        self.layout.addLayout(grid)
        self.layout.addSpacing(20)

    def setup_control_bar(self):
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.create_btn("🏠 Home", "KEY_HOME"))
        h_layout.addWidget(self.create_btn("↩ Back", "KEY_BACK"))
        h_layout.addWidget(self.create_btn("☰ Menu", "KEY_MENU"))
        self.layout.addLayout(h_layout)

    def setup_volume_bar(self):
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.create_btn("🔉 Vol−", "KEY_VOLUME_DOWN"))
        h_layout.addWidget(self.create_btn("🔇 Mute", "KEY_MUTE"))
        h_layout.addWidget(self.create_btn("🔊 Vol+", "KEY_VOLUME_UP"))
        self.layout.addLayout(h_layout)

    def setup_media_controls(self):
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.create_btn("⏮ Prev", "KEY_MEDIA_PREVIOUS"))
        h_layout.addWidget(self.create_btn("⏯ Play/Pause", "KEY_MEDIA_PLAY_PAUSE"))
        h_layout.addWidget(self.create_btn("⏭ Next", "KEY_MEDIA_NEXT"))
        self.layout.addLayout(h_layout)

    def setup_power_controls(self):
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.create_btn("⏻ Power", "KEY_POWER"))
        h_layout.addWidget(self.create_btn("💤 Sleep", "KEY_SLEEP"))
        self.layout.addLayout(h_layout)
