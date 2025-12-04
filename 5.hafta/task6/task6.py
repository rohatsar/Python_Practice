import cv2
import numpy as np

cam_cappp = cv2.VideoCapture(0)

# Başlangıç için tahmini HSV aralığı (fosforlu sarı civarı)
h_low, s_low, v_low = 20, 100, 100
h_high, s_high, v_high = 40, 255, 255

logo = cv2.imread(r"C:\Users\Rohat\Desktop\Kaan\5.hafta\task6\besiktas.webp", cv2.IMREAD_UNCHANGED)
if logo is None:
    print("❌ Logo bulunamadi, dosya adini/yolunu kontrol et.")
    exit()

logo_height, logo_width = logo.shape[:2]

prev_pts = None
smooth_factor = 0.2
kernel = np.ones((5, 5), np.uint8)

# ==== Trackbar penceresi ====
def nothing(x):
    pass

cv2.namedWindow("Mask")
cv2.namedWindow("HSV Controls")

cv2.createTrackbar("H_low", "HSV Controls", h_low, 179, nothing)
cv2.createTrackbar("S_low", "HSV Controls", s_low, 255, nothing)
cv2.createTrackbar("V_low", "HSV Controls", v_low, 255, nothing)
cv2.createTrackbar("H_high", "HSV Controls", h_high, 179, nothing)
cv2.createTrackbar("S_high", "HSV Controls", s_high, 255, nothing)
cv2.createTrackbar("V_high", "HSV Controls", v_high, 255, nothing)

while True:
    ret, frame = cam_cappp.read()
    if not ret:
        break

    # Trackbar değerlerini oku
    h_low = cv2.getTrackbarPos("H_low", "HSV Controls")
    s_low = cv2.getTrackbarPos("S_low", "HSV Controls")
    v_low = cv2.getTrackbarPos("V_low", "HSV Controls")
    h_high = cv2.getTrackbarPos("H_high", "HSV Controls")
    s_high = cv2.getTrackbarPos("S_high", "HSV Controls")
    v_high = cv2.getTrackbarPos("V_high", "HSV Controls")

    lower_color = np.array([h_low, s_low, v_low])
    upper_color = np.array([h_high, s_high, v_high])

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_color, upper_color)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        if cv2.contourArea(cnt) > 500:
            epsilon = 0.02 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)

            if len(approx) == 4:
                pts_marker = np.float32([pt[0] for pt in approx])

                if prev_pts is None:
                    smooth_pts = pts_marker
                else:
                    smooth_pts = (1 - smooth_factor) * prev_pts + smooth_factor * pts_marker

                prev_pts = smooth_pts

                pts_logo = np.float32([
                    [0, 0],
                    [logo_width, 0],
                    [logo_width, logo_height],
                    [0, logo_height]
                ])

                matrix = cv2.getPerspectiveTransform(pts_logo, smooth_pts)
                warped_logo = cv2.warpPerspective(logo, matrix, (frame.shape[1], frame.shape[0]))

                if logo.shape[2] == 4:
                    alpha = warped_logo[:, :, 3] / 255.0
                    for c in range(0, 3):
                        frame[:, :, c] = alpha * warped_logo[:, :, c] + (1 - alpha) * frame[:, :, c]
                else:
                    gray_logo = cv2.cvtColor(warped_logo, cv2.COLOR_BGR2GRAY)
                    _, mask_logo = cv2.threshold(gray_logo, 1, 255, cv2.THRESH_BINARY)
                    mask_inv = cv2.bitwise_not(mask_logo)
                    frame_bg = cv2.bitwise_and(frame, frame, mask=mask_inv)
                    logo_fg = cv2.bitwise_and(warped_logo, warped_logo, mask=mask_logo)
                    frame = cv2.add(frame_bg, logo_fg)

    cv2.imshow("Augmented Reality", frame)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam_cappp.release()
cv2.destroyAllWindows()
