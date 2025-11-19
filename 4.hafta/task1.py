from datetime import datetime

class BankaHesabi:
    def __init__(self, hesap_no, bakiye, hesap_turu, hesap_acilis_tarihi=None):
        # Hesabın temel bilgilerini burada tutuyor
        self.hesap_no = hesap_no
        self.bakiye = bakiye
        self.hesap_turu = hesap_turu.lower()
        # Tarih verilmezse hesap açılışını şu an olarak kaydediyor
        self.hesap_acilis_tarihi = hesap_acilis_tarihi or datetime.now()
        # Yapılan işlemleri tarih-saat ile kaydedeceğimiz liste
        self.islem_gecmisi = []

    def __str__(self):
        # Hesabı print() ile yazdırınca gözükecek olan özet bilgi
        return f"{self.hesap_no} nolu hesap – Bakiye: {self.bakiye} TL – Tür: {self.hesap_turu.capitalize()}"

    def __add__(self, diger):
        # İki hesabın bakiyesini topluyoruz. Yeni hesap oluşturmuyor, sadece toplama değeri döndürüyor.
        return self.bakiye + diger.bakiye

    def para_yatir(self, miktar):
        # Pozitif miktar kontrolü
        if miktar > 0:
            self.bakiye += miktar
            # İşlemi geçmişe kaydediyor
            self.islem_gecmisi.append((datetime.now(), f"Para yatırıldı: {miktar} TL"))

    def para_cek(self, miktar):
        # Yeterli bakiye yoksa işlem yapılmıyor, sadece uyarı dönüyor
        if miktar > self.bakiye:
            self.islem_gecmisi.append((datetime.now(), f"Yetersiz bakiye – Çekim denemesi: {miktar} TL"))
            return "Yetersiz bakiye"
        # Bakiye yeterliyse para çekiliyor
        self.bakiye -= miktar
        # İşlem geçmişine kayıt
        self.islem_gecmisi.append((datetime.now(), f"Para çekildi: {miktar} TL"))

    def hesap_raporu(self):
        # İşlem geçmişindeki her kaydı okunabilir hâle getirip string olarak döndürüyor
        rapor = []
        for zaman, islem in self.islem_gecmisi:
            rapor.append(f"{zaman.strftime('%Y-%m-%d %H:%M:%S')} - {islem}")
        return "\n".join(rapor)