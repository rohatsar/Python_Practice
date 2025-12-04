import cv2
import numpy as np



# HSV aralığı (kırmızımsı bir nesne için örnek)

lower_color1 = np.array([0, 120, 70])
upper_color1 = np.array([10, 255, 255])
lower_color2 = np.array([170, 120, 70])
upper_color2 = np.array([180, 255, 255])

video_path = r"C:\Users\Rohat\Desktop\Kaan\5.hafta\task3\Ahmet Kaya-Darday_m.mp3"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Video acilamadi, path'i kontrol et:", video_path)
    exit()

# Pencereyi tam ekran yap
window_name = "Shape & Color Detective - Rohat"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    ret, frame = cap.read()
    if not ret:
        break

   
    # frame = cv2.resize(frame, (1280, 720))

    # BGR -> HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Kırmızının 2 aralığını birleştir (daha stabil)
    mask1 = cv2.inRange(hsv, lower_color1, upper_color1)
    mask2 = cv2.inRange(hsv, lower_color2, upper_color2)
    mask = cv2.bitwise_or(mask1, mask2)

    # Gürültü azaltma: blur + açma-kapama (morph open/close)
    mask = cv2.GaussianBlur(mask, (7, 7), 0)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)

    # Konturlar
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Küçük gürültüleri at
    contours = [c for c in contours if cv2.contourArea(c) > 800]

    # Hepsini hafifçe çiz (yeşil)
    for cnt in contours:
        cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)

    if contours:
        # EN BÜYÜK objeyi bul
        largest = max(contours, key=cv2.contourArea)

        # Bounding box
        x, y, w, h = cv2.boundingRect(largest)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)

        # Merkez noktayı işaretle
        cx, cy = x + w // 2, y + h // 2
        cv2.circle(frame, (cx, cy), 5, (0, 255, 255), -1)

        # Şekil tespiti
        peri = cv2.arcLength(largest, True)
        approx = cv2.approxPolyDP(largest, 0.02 * peri, True)

        shape = "Unknown"
        vertices = len(approx)

        if vertices == 3:
            shape = "Triangle"
        elif vertices == 4:
            # Kare mi, dikdörtgen mi bak (aspect ratio)
            aspect_ratio = float(w) / h
            if 0.9 < aspect_ratio < 1.1:
                shape = "Square"
            else:
                shape = "Rectangle"
        elif vertices > 6:
            shape = "Circle"

        # Boyut bilgisini de yaz (w,h)
        label = f"{shape} ({w}x{h})"
        cv2.putText(frame, label, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0, 0, 255), 2)

        # Ekranın sol üstüne koordinat yaz
        cv2.putText(frame, f"Center: ({cx}, {cy})",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (255, 255, 255), 2)

    cv2.imshow(window_name, frame)

    key = cv2.waitKey(30) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
