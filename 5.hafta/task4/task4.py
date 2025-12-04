import cv2
import numpy as np

# Yüz Algılama için Haar Cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# PNG Yükleme Fonksiyonu (ARGB destekli) 
def load_png(path):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print("❌ PNG bulunamadı:", path)
        exit()
    return img

glasses_png = load_png(r"C:\Users\Rohat\Desktop\Kaan\5.hafta\task4\glasses.png")
crown_png = load_png(r"C:\Users\Rohat\Desktop\Kaan\5.hafta\task4\crown.png")
moustache_png = load_png(r"C:\Users\Rohat\Desktop\Kaan\5.hafta\task4\moustache.png")

# PNG Overlay Fonksiyonu 
def overlay_image(background, overlay, x, y, overlay_width):
    # Ölçeklendir
    scale = overlay_width / overlay.shape[1]
    new_h = int(overlay.shape[0] * scale)
    resized = cv2.resize(overlay, (overlay_width, new_h), interpolation=cv2.INTER_AREA)

    # Alfa kanalı ayır
    if resized.shape[2] == 4:
        alpha = resized[:, :, 3] / 255.0
        rgb = resized[:, :, :3]
    else:
        alpha = np.ones((resized.shape[0], resized.shape[1]))
        rgb = resized

    # Arka plan sınırlarını kontrol et
    for c in range(3):
        bg_region = background[y:y + new_h, x:x + overlay_width, c]
        bg_region[:] = (1 - alpha) * bg_region + alpha * rgb[:, :, c]

# Webcam Başlat
cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print("❌ Webcam açılamadı.")
    exit()

while True:
    ret, frame = cam.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.15, 6)

    for (x, y, w, h) in faces:

        # ========== Gözlük ==========
        glasses_w = int(w * 0.9)
        glasses_x = x + int(w * 0.05)
        glasses_y = y + int(h * 0.32)
        overlay_image(frame, glasses_png, glasses_x, glasses_y, glasses_w)

        # ========== Taç ==========
        crown_w = int(w * 1.2)
        crown_x = x - int(w * 0.1)
        crown_y = y - int(h * 0.75)
        overlay_image(frame, crown_png, crown_x, crown_y, crown_w)

        # ========== Bıyık ==========
        moust_w = int(w * 0.55)
        moust_x = x + int(w * 0.23)
        moust_y = y + int(h * 0.65)
        overlay_image(frame, moustache_png, moust_x, moust_y, moust_w)

        # Yüz kutusu (istersen kapatabilirsin)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 180), 2)

    cv2.imshow("Rohat Filter Cam", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
