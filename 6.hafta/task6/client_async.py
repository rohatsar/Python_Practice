import asyncio
import socketio

# Asenkron Socket.IO client
sio = socketio.AsyncClient()


@sio.event
async def connect():
    print("Connected to async server")


@sio.event
async def disconnect():
    print("Disconnected from async server")


async def main():
    # Sunucuya bağlan
    await sio.connect("http://localhost:5000")

    try:
        # Her 1 saniyede bir get_time isteği gönder
        while True:
            response = await sio.call("get_time")
            server_time = response.get("server_time", None)
            print("Server time:", server_time)
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping client...")
    finally:
        await sio.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
