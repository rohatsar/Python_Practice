import socketio

sio = socketio.Client()
USERNAME = "Rohat"

# chat namespace 

@sio.on("connect", namespace="/chat")
def on_connect_chat():
    print("Connected to /chat as", USERNAME)


@sio.on("disconnect", namespace="/chat")
def on_disconnect_chat():
    print("Disconnected from /chat")


@sio.on("chat_message", namespace="/chat")
def on_chat_message(data):
    text = data.get("text", "")
    print("CHAT >>", text)


# status namespace 

@sio.on("connect", namespace="/status")
def on_connect_status():
    print("Connected to /status")

    # health_check isteği gönder ve cevabı callback ile al
    def ack(response):
        print("Status health_check response:", response)

    sio.emit("health_check", namespace="/status", callback=ack)


@sio.on("disconnect", namespace="/status")
def on_disconnect_status():
    print("Disconnected from /status")


#  main 

if __name__ == "__main__":
    # İki namespace'e birden bağlan
    sio.connect("http://localhost:5000", namespaces=["/chat", "/status"])

    try:
        while True:
            msg = input("You (/chat): ").strip()
            if not msg:
                continue

            payload = {
                "username": USERNAME,
                "message": msg
            }
            sio.emit("chat_message", payload, namespace="/chat")
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        sio.disconnect()
