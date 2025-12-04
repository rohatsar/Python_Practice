import cv2
import numpy as np

# Project 5: Motion Tracker (Improved Version)

video_capp = cv2.VideoCapture(r"C:\Users\Rohat\Desktop\Kaan\5.hafta\task5\dog running slow motion.mp4")
background_sub = cv2.createBackgroundSubtractorMOG2()
kernel = np.ones((5, 5), np.uint8)

zone_top_left = (100, 100)
zone_bottom_right = (400, 400)
path_points = []

while True:
    ret, frame = video_capp.read()

    if not ret:
        # ---- Video bittiğinde ekranda son frame kalsın ----
        print("Video bitti. Cikmak icin 'q' basin.")
        while True:
            cv2.imshow("Motion Tracker", frame)
            if cv2.waitKey(0) & 0xFF == ord('q'):
                video_capp.release()
                cv2.destroyAllWindows()
                exit()
        break

    # ---- Background subtraction ----
    frame_mask = background_sub.apply(frame)
    frame_mask = cv2.morphologyEx(frame_mask, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(frame_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    center = None
    max_area = 500

    # ---- Hareket tespiti ----
    for cnt in contours:
        if cv2.contourArea(cnt) > max_area:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # ---- En büyük objeyi takip et ----
    if contours:
        largest = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest) > max_area:
            x, y, w, h = cv2.boundingRect(largest)
            center = (x + w // 2, y + h // 2)

    # ---- Path çizdirme ----
    if center is not None:
        path_points.append(center)

    for i in range(1, len(path_points)):
        cv2.line(frame, path_points[i - 1], path_points[i], (255, 0, 0), 2)

    # ---- Güvenlik bölgesi ----
    cv2.rectangle(frame, zone_top_left, zone_bottom_right, (0, 0, 255), 2)

    if center is not None:
        cx, cy = center
        if zone_top_left[0] < cx < zone_bottom_right[0] and zone_top_left[1] < cy < zone_bottom_right[1]:
            cv2.putText(frame, "ALERT!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    # ---- Görüntüleri göster ----
    cv2.imshow("Motion Tracker", frame)
    cv2.imshow("Mask", frame_mask)

    # ---- Çıkış tuşu ----
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

video_capp.release()
cv2.destroyAllWindows()
