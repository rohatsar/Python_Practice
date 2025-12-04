import cv2
import numpy as np
import os

print(os.getcwd())     
print(os.listdir())

# ---- Ayarlar ----
img_path = r"C:\Users\Rohat\Desktop\Kaan\5.hafta\task1\colorful_landscape.webp"


img = cv2.imread(img_path)

if img is None:
    print("Görsel bulunamadı, yolu kontrol et:", img_path)
    raise SystemExit()

# 1) Orijinal görüntü
cv2.imshow("Rohat - Orijinal", img)

# 2) Boyut / kanal bilgisi
h, w, ch = img.shape
print(f"Genislik: {w}, Yukseklik: {h}, Kanal: {ch}")

# 3) Kanalları ayır
b, g, r = cv2.split(img)

cv2.imshow("Mavi (B)", b)
cv2.imshow("Yesil (G)", g)
cv2.imshow("Kirmizi (R)", r)

# 4) R ve B kanal degisimi
rb_swapped = cv2.merge([r, g, b])
cv2.imshow("R-B Degistirilmis", rb_swapped)

# 5) Kirpma & yeniden boyutlandirma
# köşeden değil, hafif yan ortadan bir bölge alalım
y1 = h // 5
y2 = y1 + h // 2
x1 = w // 6
x2 = x1 + w // 2

cropped = img[y1:y2, x1:x2]
resized = cv2.resize(cropped, (220, 220))
cv2.imshow("Kirp + Resize (Rohat Style)", resized)

# 6) Gri tonlama
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow("Gri Tonlama", gray)

# ---- Özel Filtre 1: Sicak ton (Warm) ----
warm = img.copy().astype(np.int16)

# biraz sarımsı ve kırmızılı bir hava katsın
warm[:, :, 2] += 35   # R
warm[:, :, 1] += 15   # G
warm[:, :, 0] -= 15   # B

warm = np.clip(warm, 0, 255).astype(np.uint8)
cv2.imshow("Sicak Ton - Rohat", warm)

# ---- Özel Filtre 2: Vintage / hafif soluk film efekti ----
# önce hafif blur, sonra kontrast/parlaklık oynama
blur = cv2.GaussianBlur(img, (17, 17), 0)

alpha = 0.65  # kontrast
beta = -20    # parlaklığı biraz düşür
vintage = cv2.convertScaleAbs(blur, alpha=alpha, beta=beta)

# biraz da orijinalle karıştıralım
vintage_mix = cv2.addWeighted(img, 0.5, vintage, 0.5, 0)
cv2.imshow("Vintage - Rohat Mix", vintage_mix)

# bonus: hafif yatay çevirilmiş versiyon (tamamen ekstra, projeyi zengin gösterir)
flipped = cv2.flip(img, 1)
cv2.imshow("Ayna Efektli (Ekstra)", flipped)

cv2.waitKey(0)
cv2.destroyAllWindows()
