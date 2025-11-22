from collections import Counter
import math
# Öğrenci Not Sistemi (Inheritance + Collections)
# Ogrenci base class ve LisansOgrencisi, YuksekLisansOgrencisi subclass’ları oluşturun.
# Ogrenci: ad, soyad, ogrenci_no, ders_notlari (dict)
# not_ekle: ders adı ve not listesi alacak, Counter ile not istatistiği tutsun
# ortalama_hesaplama : math modülü ile yuvarlama (math.ceil ya da math.floor)
# LisansOgrencisi: ortalama hesaplama methodunu override edip farklı formül kullanacak
# YuksekLisansOgrencisi: Not değerlendirme kriterleri farklı olacak.
# Örnek: ogrenci1.not_ekle(“Matematik”, [85, 90, 78])

class Ogrenci:
    def __init__(self, ad, soyad, ogrenci_no, ders_notlari=None):
        self.ad = ad
        self.soyad = soyad
        self.ogrenci_no = ogrenci_no
        self.ders_notlari = ders_notlari or {}

    def not_ekle(self, ders_adi, not_listesi):
        """Derse not ekleme ve not dağılımını Counter ile gösterme"""
        if ders_adi not in self.ders_notlari:
            self.ders_notlari[ders_adi] = not_listesi
        else:
            self.ders_notlari[ders_adi] += not_listesi

        ders_istatistik = Counter(self.ders_notlari[ders_adi])
        print(f"{ders_adi} not dağılımı: {ders_istatistik}")
        return ders_istatistik  

    def ortalama_hesaplama(self, ders_adi):
        """Ders ortalamasını hesaplar, math.ceil ile yuvarlar"""
        if ders_adi not in self.ders_notlari:
            print("Böyle bir ders bulunmamaktadır")
            return None

        not_listesi = self.ders_notlari[ders_adi]
        if len(not_listesi) == 0:
            print(f"{ders_adi} için hiç not girilmemiş")
            return None

        not_ortalama = sum(not_listesi) / len(not_listesi)
        return math.ceil(not_ortalama)


class LisansOgrencisi(Ogrenci):
    def ortalama_hesaplama(self, ders_adi):
        """
        Lisans öğrencisi için özel ortalama:
        - Eğer en az iki not varsa, vize %40, final %60 ağırlık
        - Yoksa standart ortalama
        """
        if ders_adi not in self.ders_notlari:
            print("Böyle bir ders bulunmamaktadır")
            return None

        not_listesi = self.ders_notlari[ders_adi]
        if len(not_listesi) == 0:
            print(f"{ders_adi} için hiç not girilmemiş")
            return None

        if len(not_listesi) >= 2:
            vize, final = not_listesi[0], not_listesi[1]
            ortalama = vize * 0.4 + final * 0.6
        else:
            ortalama = sum(not_listesi) / len(not_listesi)

        return math.floor(ortalama)


class YuksekLisansOgrencisi(Ogrenci):
    def ortalama_hesaplama(self, ders_adi):
        """
        Yüksek Lisans öğrencisi için farklı değerlendirme:
        - Tüm notlar eşit ağırlıkta alınır
        - math.floor ile yuvarlanır
        """
        if ders_adi not in self.ders_notlari:
            print("Böyle bir ders bulunmamaktadır")
            return None

        not_listesi = self.ders_notlari[ders_adi]
        if len(not_listesi) == 0:
            print(f"{ders_adi} için hiç not girilmemiş")
            return None

        not_ortalama = sum(not_listesi) / len(not_listesi)
        return math.floor(not_ortalama)

def main():
    print("=== Öğrenci Not Sistemi Test ===")

    # Öğrenciler
    ogr1 = Ogrenci("Ali", "Yılmaz", 123)
    lisans1 = LisansOgrencisi("Ayşe", "Demir", 456)
    yuksek1 = YuksekLisansOgrencisi("Mehmet", "Kara", 789)

    # NOT EKLEME
    print("\n--- Not Ekleme ---")
    ogr1.not_ekle("Matematik", [85, 90, 78])
    lisans1.not_ekle("Fizik", [70, 80])
    yuksek1.not_ekle("Yazılım", [90, 95, 85])

    # ORTALAMA HESAPLAMA
    print("\n--- Ortalama Hesaplama ---")

    print(f"Ali - Matematik ortalama: {ogr1.ortalama_hesaplama('Matematik')}")
    print(f"Ayşe (Lisans) - Fizik ortalama: {lisans1.ortalama_hesaplama('Fizik')}")
    print(f"Mehmet (Yüksek Lisans) - Yazılım ortalama: {yuksek1.ortalama_hesaplama('Yazılım')}")

    # Aynı derse tekrar not ekleme testi
    print("\n--- Ek Not Ekleme (Counter Test) ---")
    ogr1.not_ekle("Matematik", [85, 100])  # tekrar ekleniyor

    print(f"Ali - Matematik yeni ortalama: {ogr1.ortalama_hesaplama('Matematik')}")


if __name__ == "__main__":
    main()
