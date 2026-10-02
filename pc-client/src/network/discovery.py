import socket
import time
from PySide6.QtCore import QObject, Signal, QThread
from zeroconf import ServiceBrowser, ServiceListener, Zeroconf

class TVListener(ServiceListener):
    def __init__(self, callback):
        self.callback = callback

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        pass

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} removed")

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        if info:
            ip = socket.inet_ntoa(info.addresses[0])
            port = info.port
            self.callback(name, ip, port)

class DiscoveryWorker(QObject):
    tv_found = Signal(str, str, int)
    
    def __init__(self):
        super().__init__()
        self.zeroconf = None
        self.browser = None
        
    def start_discovery(self):
        self.zeroconf = Zeroconf()
        listener = TVListener(self.on_tv_found)
        self.browser = ServiceBrowser(self.zeroconf, "_sonytv._tcp.local.", listener)
        
    def on_tv_found(self, name, ip, port):
        self.tv_found.emit(name, ip, port)
        
    def stop(self):
        if self.zeroconf:
            self.zeroconf.close()

class DiscoveryManager(QObject):
    tv_found = Signal(str, str, int)

    def __init__(self):
        super().__init__()
        self.worker = DiscoveryWorker()
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        
        self.worker.tv_found.connect(self.tv_found)
        self.thread.started.connect(self.worker.start_discovery)
        
    def start(self):
        self.thread.start()
        
    def stop(self):
        self.worker.stop()
        self.thread.quit()
        self.thread.wait()
