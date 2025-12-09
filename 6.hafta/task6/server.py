import time
import socketio
from aiohttp import web

# Asenkron Socket.IO server 
sio = socketio.AsyncServer(async_mode="aiohttp")
app = web.Application()
sio.attach(app)


@sio.event
async def connect(sid, environ):
    print("Client connected:", sid)


@sio.event
async def disconnect(sid):
    print("Client disconnected:", sid)


@sio.event
async def get_time(sid):
    """
    İstemci bu event'i çağırdığında,
    sunucu mevcut zamanı döner.
    """
    current_time = time.time()
    print(f"get_time requested from {sid}, time: {current_time}")
    return {"server_time": current_time}


if __name__ == "__main__":
    print("Async Socket.IO server is running on port 5000...")
    web.run_app(app, host="0.0.0.0", port=5000)
