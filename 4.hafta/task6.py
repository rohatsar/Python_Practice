import math
from datetime import datetime, timedelta


class Personel:
    def __init__(self, ad, soyad, maas, departman, ise_baslama_tarihi):
        self.ad = ad
        self.soyad = soyad
        self.maas = maas
        self.departman = departman

        # Tarihi string olarak verirsen "YYYY-MM-DD" formatından datetime'a çeviriyorum
        if isinstance(ise_baslama_tarihi, str):
            self.ise_baslama_tarihi = datetime.strptime(ise_baslama_tarihi, "%Y-%m-%d")
        else:
            self.ise_baslama_tarihi = ise_baslama_tarihi

    def __str__(self):
        return f"{self.ad} {self.soyad} - {self.departman} - Maaş: {self.maas} TL"

    def calisma_suresi_gun(self):
        """Toplam çalışma süresini gün olarak döner."""
        bugun = datetime.now()
        fark = bugun - self.ise_baslama_tarihi
        return fark.days

    def zam_hesapla(self):
        """
        Kıdeme göre zam oranı belirliyoruz.
        < 1 yıl  : %5
        1-3 yıl  : %10
        3+ yıl   : %20
        """
        gun = self.calisma_suresi_gun()
        yil = gun // 365

        if yil < 1:
            oran = 0.05
        elif yil < 3:
            oran = 0.10
        else:
            oran = 0.20

        return oran  # 0.10 gibi bir oran dönüyor

    def izin_hesapla(self):
        """
        Çalışılan süreye göre izin gününü hesaplıyoruz.
        < 1 yıl  : 10 gün
        1-5 yıl  : 14 gün
        5+ yıl   : 20 gün
        timedelta olarak döndürüyorum.
        """
        gun = self.calisma_suresi_gun()
        yil = gun // 365

        if yil < 1:
            izin_gun = 10
        elif yil < 5:
            izin_gun = 14
        else:
            izin_gun = 20

        # timedelta kullanarak izin süresini temsil edelim
        return timedelta(days=izin_gun)

    def __eq__(self, diger):
        """Maaşlar aynı mı diye kontrol ediyor."""
        return self.maas == diger.maas

    def __gt__(self, diger):
        """
        Daha uzun süredir çalışan > olsun istiyorsak:
        Daha eski başlayan kişi > olmalı.
        Yani başlangıç tarihi daha küçük (daha eski) olan daha kıdemli.
        """
        return self.ise_baslama_tarihi < diger.ise_baslama_tarihi


class Yonetici(Personel):
    def __init__(self, ad, soyad, maas, departman, ise_baslama_tarihi, sorumlu_oldugu_kisiler=None):
        super().__init__(ad, soyad, maas, departman, ise_baslama_tarihi)
        # Liste verilmezse boş listeyle başlat
        self.sorumlu_oldugu_kisiler = sorumlu_oldugu_kisiler or []

    def bonus_hesapla(self):
        """
        Basit bir bonus mantığı:
        Her sorumlu olduğu kişi için 500 TL bonus.
        """
        kisi_sayisi = len(self.sorumlu_oldugu_kisiler)
        bonus = kisi_sayisi * 500
        return bonus


class Gelistirici(Personel):
    def __init__(self, ad, soyad, maas, departman, ise_baslama_tarihi, teknoloji_stack=None):
        super().__init__(ad, soyad, maas, departman, ise_baslama_tarihi)
        # Kullanılan teknolojileri liste olarak tutuyor
        self.teknoloji_stack = teknoloji_stack or []

    def prim_hesapla(self, proje_sayisi):
        """
        Proje bazlı prim:
        Her proje için 1000 TL temel prim,
        Üstüne bildiği teknoloji sayısı * 100 TL ek.
        """
        temel_prim = 1000
        ekstra = len(self.teknoloji_stack) * 100
        toplam_prim = proje_sayisi * (temel_prim + ekstra)
        return toplam_prim



if __name__ == "__main__":
    personel1 = Yonetici(
        "Rohat",
        "Sarigul",
        120000,
        "IT",
        "2020-03-15",
        ["Mert", "Deniz"]
    )

    personel2 = Gelistirici(
        "Meleksu",
        "Böyük",
        95000,
        "Yazılım",
        "2021-06-20",
        ["Python", "JavaScript", "SQL"]
    )

    print(personel1)
    print(personel2)

    print(f"Kıdemlı olan kim? {personel1 > personel2}")  
    print(f"Zam oranı (Rohat): {personel1.zam_hesapla()*100:.1f}%")
    print(f"Zam oranı (Meleksu): {personel2.zam_hesapla()*100:.1f}%")

    print(f"Rohat'ın izin süresi: {personel1.izin_hesapla().days} gün")
    print(f"Meleksu'nun izin süresi: {personel2.izin_hesapla().days} gün")

    print(f"Rohat'ın bonusu: {personel1.bonus_hesapla()} TL")
    print(f"Meleksu'nun primi: {personel2.prim_hesapla(proje_sayisi=3)} TL")

    print(f"Maaşlar eşit mi? {personel1 == personel2}")
