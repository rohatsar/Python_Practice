import random
import string
from datetime import datetime
import math

# E-Ticaret Sistemi (OOP Composition)
# Urun class: isim, fiyat, stok(property decorator ile kontrol), barkod(random modülü ile oluşturulacak)
# Musteri class: ad, email, sepet (ürün listesi), sipariş geçmişi
# Siparis class: sipariş no (random), sipariş tarihi (datetime), toplam tutar
# odeme_yap methodu: math modülü ile KDV hesaplayacak (%18)
# stok_guncelle methodu: Ürün satın alındığında stokları güncelleyecek.
# __contains__ methodu: müşterinin sepetinde belirli ürün olup olmadığını kontrol edecek.

class Urun:
    def __init__(self, isim, fiyat, stok):
        self.isim = isim
        self.fiyat = fiyat
        self._stok = stok
        self.barkod = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

    @property
    def stok(self):
        return self._stok

    @stok.setter
    def stok(self, yeni_stok):
        if yeni_stok < 0:
            print("Stok değeri negatif olamaz!")
        else:
            self._stok = yeni_stok


class Musteri:
    def __init__(self, ad, email):
        self.ad = ad
        self.email = email
        self.sepet = []
        self.siparis_gecmisi = []

    def __contains__(self, urun):
        return urun in self.sepet

    def stok_guncelle(self, urun):
        if urun.stok > 0:
            urun.stok -= 1
            self.siparis_gecmisi.append(urun)
            try:
                self.sepet.remove(urun)
            except ValueError:
                # Ürün sepette yoksa hata verme
                pass
            print(f"{urun.isim} siparişi başarıyla oluşturuldu. Kalan stok: {urun.stok}")
        else:
            print(f"Seçtiğiniz ürün ({urun.isim}) stoğu bulunmamaktadır.")


class Siparis:
    def __init__(self, musteri, urunler):
        self.musteri = musteri
        self.urunler = urunler
        self.siparis_no = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        self.siparis_tarihi = datetime.now()
        self.toplam_tutar = 0

    def toplam_tutar_hesapla(self):
        self.toplam_tutar = sum(item.fiyat for item in self.urunler)

    def odeme_yap(self):
        self.toplam_tutar_hesapla()
        self.odenecek_tutar = self.toplam_tutar * 1.18  # %18 KDV
        for urun in self.urunler:
            self.musteri.stok_guncelle(urun)
        print(f"Sipariş tamamlandı, toplam ödenecek tutar: {self.odenecek_tutar:.2f} TL")

def main():
    # Ürünleri oluşturalım
    urun1 = Urun("Telefon", 15000, 3)
    urun2 = Urun("Kulaklık", 500, 10)
    urun3 = Urun("Klavye", 1200, 5)

    # Müşteri oluştur
    musteri = Musteri("Başak", "basak@example.com")

    # Sepete ürün ekleyelim
    musteri.sepet.append(urun1)
    musteri.sepet.append(urun2)

    print("\n--- Sepet Kontrolü ---")
    print("Telefon sepette mi?", urun1 in musteri)
    print("Klavye sepette mi?", urun3 in musteri)

    # Sipariş oluştur
    siparis = Siparis(musteri, musteri.sepet)

    # Ödeme yap
    print("\n--- Ödeme ve Stok Güncelleme ---")
    siparis.odeme_yap()

    # Sipariş geçmişi
    print("\n--- Sipariş Geçmişi ---")
    for urun in musteri.siparis_gecmisi:
        print(f"{urun.isim} satın alındı, kalan stok: {urun.stok}")

    # Sipariş Özeti
    print("\n--- Sipariş Özeti ---")
    print(f"Sipariş No: {siparis.siparis_no}")
    print(f"Sipariş Tarihi: {siparis.siparis_tarihi}")
    print(f"Toplam Tutar (KDV Dahil): {siparis.odenecek_tutar:.2f} TL")


if __name__ == "__main__":
    main()
