import socketio

sio = socketio.Client()

USERNAME = "Rohat"


@sio.event
def connect():
    print("Connected to chat server as:", USERNAME)
    print("Type your messages and press Enter. Ctrl+C to exit.")


@sio.on("new_message")
def handle_new_message(data):
    text = data.get("text", "")
    print(">>", text)


@sio.event
def disconnect():
    print("Disconnected from server")


if __name__ == "__main__":
    sio.connect("http://localhost:5000")

    try:
        while True:
            msg = input("You: ").strip()
            if not msg:
                continue

            payload = {
                "username": USERNAME,
                "message": msg
            }
            sio.emit("chat_message", payload)
    except KeyboardInterrupt:
        print("\nExiting chat...")
    finally:
        sio.disconnect()
