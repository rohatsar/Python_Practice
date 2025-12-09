import socketio

sio = socketio.Client()

USERNAME = "Rohat"
current_room = None


@sio.event
def connect():
    print("Connected to server as:", USERNAME)
    print("You can join 'roomA' or 'roomB'.")


@sio.on("room_info")
def handle_room_info(data):
    text = data.get("text", "")
    print("INFO:", text)


@sio.on("room_message")
def handle_room_message(data):
    text = data.get("text", "")
    print(">>", text)


@sio.event
def disconnect():
    print("Disconnected from server")


if __name__ == "__main__":
    sio.connect("http://localhost:5000")

    try:
        # Odayı seç
        while True:
            room = input("Join which room? (roomA / roomB): ").strip()
            if room in ["roomA", "roomB"]:
                break
            print("Please type 'roomA' or 'roomB'.")

        join_data = {
            "room": room,
            "username": USERNAME
        }
        current_room = room
        sio.emit("join_room", join_data)

        print(f"You joined {current_room}. Now you can send messages.")
        print("Type messages and press Enter. Ctrl+C to exit.\n")

        # Mesaj gönderme döngüsü
        while True:
            msg = input("You: ").strip()
            if not msg:
                continue

            payload = {
                "room": current_room,
                "username": USERNAME,
                "message": msg
            }
            sio.emit("room_message", payload)

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        sio.disconnect()
