import cv2
import numpy as np
import os

print(os.getcwd())
print(os.listdir())

#  Global Ayarlar 
drawing = False
brush_size = 6
paint_color = (0, 0, 255)  # BGR (kırmızı)

def draw_paint(event, x, y, flags, param):
    global drawing
    canvas = param

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        cv2.circle(canvas, (x, y), brush_size, paint_color, -1)

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        cv2.circle(canvas, (x, y), brush_size, paint_color, -1)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

# WEBCAM KISMI 
cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print("Webcam acilamadi.")
else:
    ret, frame = cam.read()
    if not ret:
        print("Webcam'den frame okunamadi.")
    else:
        canvas_cam = np.zeros_like(frame)

        cv2.namedWindow("Rohat Webcam")
        cv2.setMouseCallback("Rohat Webcam", draw_paint, canvas_cam)

        screenshot_count = 0

        while True:
            ret, frame = cam.read()
            if not ret:
                break

            # Çizim canvas'ını görüntüyle birleştir
            merged = cv2.addWeighted(frame, 1.0, canvas_cam, 1.0, 0)

            # Şekiller + yazılar
            cv2.rectangle(merged, (20, 20), (220, 120), (0, 180, 255), 2)
            cv2.putText(merged, "Rohat Live Cam",
                        (30, 60),
                        cv2.FONT_HERSHEY_DUPLEX,
                        0.8,
                        (0, 255, 180),
                        2)

            cv2.putText(merged, "[q] cikis  [s] ss  [c] temizle",
                        (20, merged.shape[0] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255, 255, 255),
                        1)

            cv2.imshow("Rohat Webcam", merged)

            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                break
            elif key == ord('s'):
                filename = f"webcam_ss_{screenshot_count}.png"
                cv2.imwrite(filename, merged)
                print("Webcam screenshot kaydedildi:", filename)
                screenshot_count += 1
            elif key == ord('c'):
                canvas_cam[:] = 0

    cam.release()
    cv2.destroyAllWindows()

#  VIDEO KISMI 
# deprem.mp4 dosyasi bu .py dosyayla AYNI klasorde olmali
video = cv2.VideoCapture(r"C:\Users\Rohat\Desktop\Kaan\5.hafta\task2\Kayıt 2025-10-13 111138.mp4")

if not video.isOpened():
    print("Video acilamadi. 'deprem.mp4' yolunu kontrol et.")
else:
    ret, frame = video.read()
    if not ret:
        print("Videodan frame okunamadi.")
    else:
        canvas_vid = np.zeros_like(frame)

        cv2.namedWindow("Deprem Videosu")
        cv2.setMouseCallback("Deprem Videosu", draw_paint, canvas_vid)

        screenshot_count = 0

        while True:
            ret, frame = video.read()
            if not ret:
                break

            # Çizim canvas'i ile birlestir
            merged = cv2.addWeighted(frame, 1.0, canvas_vid, 1.0, 0)

            # Şekiller + yazılar
            cv2.rectangle(merged, (30, 30), (260, 110), (255, 165, 0), 2)
            cv2.circle(merged, (350, 250), 45, (0, 200, 255), 3)

            cv2.putText(merged, "Deprem Goruntusu",
                        (40, 70),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.9,
                        (255, 255, 255),
                        2)

            cv2.putText(merged, "[q] cikis  [s] ss  [c] temizle",
                        (20, merged.shape[0] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255, 255, 255),
                        1)

            cv2.imshow("Deprem Videosu", merged)

            key = cv2.waitKey(30) & 0xFF

            if key == ord('q'):
                break
            elif key == ord('s'):
                filename = f"deprem_ss_{screenshot_count}.png"
                cv2.imwrite(filename, merged)
                print("Video screenshot kaydedildi:", filename)
                screenshot_count += 1
            elif key == ord('c'):
                canvas_vid[:] = 0

    video.release()
    cv2.destroyAllWindows()
