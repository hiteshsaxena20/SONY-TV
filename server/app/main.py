from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict

app = FastAPI(title="SONY TV Relay API")

# Simple in-memory registry for connected devices (Phase 2)
connected_devices: Dict[str, WebSocket] = {}

@app.get("/")
async def root():
    return {"status": "ok", "service": "SONY TV Relay"}

@app.websocket("/ws/{device_id}")
async def websocket_endpoint(websocket: WebSocket, device_id: str):
    await websocket.accept()
    connected_devices[device_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            # In Phase 2: Route message to paired device
            # For now, echo back
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        del connected_devices[device_id]
