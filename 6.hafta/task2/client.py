import socketio

sio = socketio.Client()


@sio.event
def connect():
    print("Connected to server")

    # Sunucuya login verisi gönder
    login_data = {
        "username": "Rohat",
        "level": 5
    }
    print("Sending login data:", login_data)
    sio.emit("login", login_data)


@sio.on("login_response")
def handle_login_response(data):
    # Sunucudan gelen cevabı yazdır
    message = data.get("message", "")
    print("Server response:", message)


@sio.event
def disconnect():
    print("Disconnected from server")


if __name__ == "__main__":
    sio.connect("http://localhost:5000")
    sio.wait()
