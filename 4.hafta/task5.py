import random
import time
import math
from collections import Counter
from datetime import datetime


class QuizUygulamasi:
    def __init__(self):
        # Soru bankasını basit tutuyorum, sözlük listesi şeklinde
        self.soru_bankasi = [
            {"soru": "Python hangi dil kategorisine girer?", "cevap": "yüksek seviye", "zorluk": "kolay"},
            {"soru": "Listelerin indekslemesi kaçtan başlar?", "cevap": "0", "zorluk": "kolay"},
            {"soru": "collections modülünde sayaç gibi çalışan sınıfın adı nedir?", "cevap": "counter", "zorluk": "orta"},
            {"soru": "Rastgele seçim için hangi modülü kullanıyoruz?", "cevap": "random", "zorluk": "orta"},
            {"soru": "Pi sayısına hangi modülden erişiriz?", "cevap": "math", "zorluk": "zor"},
        ]

        # Doğru / yanlış saymak için Counter
        self.istatistik = Counter()
        # Son quiz süresi ve puan
        self.son_sure = None
        self.son_puan = 0
        # Her sorunun detayını burada saklayacağız
        self.cevap_kayitlari = []

    def soru_sec(self, adet):
        """
        soru_bankasından rastgele 'adet' kadar soru seçer.
        """
        
        return random.sample(self.soru_bankasi, adet)

    def cevap_kontrol(self, kullanici_cevabi, dogru_cevap):
        """
        Kullanıcının cevabını kontrol eder ve Counter'a işler.
        """
        # Küçük bir normalize işlemi: baş-son boşluk kırp + küçük harf
        kullanici_cevabi = kullanici_cevabi.strip().lower()
        dogru_cevap = dogru_cevap.strip().lower()

        if kullanici_cevabi == dogru_cevap:
            self.istatistik["dogru"] += 1
            return True
        else:
            self.istatistik["yanlis"] += 1
            return False

    def puan_hesapla(self):
        """
        Zorluk seviyesine göre puan hesabı.
        kolay: katsayı 1
        orta:  katsayı 2
        zor:   katsayı 3
        """
        katsayilar = {
            "kolay": 1,
            "orta": 2,
            "zor": 3
        }

        puan = 0

        for kayit in self.cevap_kayitlari:
            if kayit["dogru_mu"]:
                zorluk = kayit["zorluk"]
                katsayi = katsayilar.get(zorluk, 1)
                # Her doğru soru 10 puan, zorlukla çarpıyor
                puan += 10 * katsayi

        # Tam sayı puan kalsın diye floor kullanıyor
        return math.floor(puan)

    def rapor_olustur(self):
        """
        Quiz sonunda detaylı rapor üretir.
        """
        tarih_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        toplam_soru = len(self.cevap_kayitlari)
        dogru = self.istatistik["dogru"]
        yanlis = self.istatistik["yanlis"]

       
        if toplam_soru > 0:
            basari_orani = (dogru / len(self.soru_bankasi)) * 100  
        else:
            basari_orani = 0

        satirlar = []
        satirlar.append(f"--- Quiz Raporu ---")
        satirlar.append(f"Tarih: {tarih_str}")
        if self.son_sure is not None:
            satirlar.append(f"Süre: {self.son_sure:.2f} saniye")
        else:
            satirlar.append("Süre bilgisi yok")

        satirlar.append(f"Toplam soru: {toplam_soru}")
        satirlar.append(f"Doğru: {dogru}  Yanlış: {yanlis}")
        satirlar.append(f"Başarı oranı: {basari_orani:.1f}%")
        satirlar.append(f"Puan: {self.son_puan}")
        satirlar.append("")
        satirlar.append("Detaylı cevaplar:")

        for i, kayit in enumerate(self.cevap_kayitlari, start=1):
            durum = "Doğru" if kayit["dogru_mu"] else "Yanlış"
            satirlar.append(
                f"{i}. {kayit['soru']} (Zorluk: {kayit['zorluk']}) -> "
                f"Doğru cevap: {kayit['dogru_cevap']} / Senin cevabın: {kayit['kullanici_cevabi']} [{durum}]"
            )

        return "\n".join(satirlar)

    def quiz_baslat(self, soru_sayisi=3):
        """
        Quiz akışını başlatır:
        - Soruları seçer
        - Süreyi tutar
        - Kullanıcıdan cevap alır
        - Sonunda rapor yazdırır
        """
        # Her quizde kayıtları sıfırlıyor
        self.cevap_kayitlari.clear()
        self.istatistik.clear()

        secilen_sorular = self.soru_sec(soru_sayisi)

        print(f"{soru_sayisi} soruluk quiz başlıyor...")
        time.sleep(0.5)

        baslangic = time.time()

        for soru in secilen_sorular:
            print("\nSoru:", soru["soru"])
            cevap = input("Cevabınız: ")

            dogru_mu = self.cevap_kontrol(cevap, soru["cevap"])

            # Her soruyu detaylı kaydediyor
            self.cevap_kayitlari.append({
                "soru": soru["soru"],
                "dogru_cevap": soru["cevap"],
                "kullanici_cevabi": cevap,
                "zorluk": soru["zorluk"],
                "dogru_mu": dogru_mu
            })

        bitis = time.time()
        self.son_sure = bitis - baslangic
        self.son_puan = self.puan_hesapla()

        print("\nQuiz bitti!")
        print(self.rapor_olustur())



if __name__ == "__main__":
    quiz = QuizUygulamasi()
    quiz.quiz_baslat(soru_sayisi=3)
