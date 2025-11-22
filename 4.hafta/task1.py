from datetime import datetime
# Banka Hesap Sistemi (Class + Dunder Methods)
# BankaHesabi adında bir class oluşturun:
# __init__ : hesap_no, bakiye, hesap_turu (vadeli/vadesiz), hesap_acilis_tarihi(datetime kullanın)
# __str__: Hesap bilgilerini döndürsün
# __add__: iki hesabın bakiyelerini toplayıp yeni bir bakiye değeri döndürmeli
# para_cek, para_yatir methodları (para_cek methodu yeterli bakiye yoksa uyarı vermeli)
# hesap_raporu methodu: tüm işlem geçmişini tarih-saat bilgisi ile göstermeli
# Örnek: print(hesap1) ”12345 nolu hesap – Bakiye: 1000 TL – Tür: Vadesiz”


class BankaHesabi:
    def __init__(self, hesap_no, bakiye, hesap_turu, hesap_acilis_tarihi):
        self.hesap_no = hesap_no
        self.bakiye = bakiye
        self.hesap_turu = hesap_turu
        self.hesap_acilis_tarihi = hesap_acilis_tarihi
        self.islem_gecmisi = []

    def __str__(self):
        return (f"{self.hesap_acilis_tarihi} tarihinden itibaren aktif olan {self.hesap_no} nolu "
                f"{self.hesap_turu} hesabının "
                f"bakiyesi {self.bakiye} TL'dir")

    def para_yatir(self, yatirilan_tutar):
        self.yatirilan_tutar = yatirilan_tutar
        self.bakiye += yatirilan_tutar
        self.islem_gecmisi.append(f"{datetime.now()} – Hesabınıza {yatirilan_tutar} TL yatırıldı")
        print(f"{yatirilan_tutar} TL başarıyla yatırıldı. Güncel bakiye: {self.bakiye} TL")

    def para_cek(self, cekilen_tutar):
        self.cekilen_tutar = cekilen_tutar

        if self.cekilen_tutar > self.bakiye:
            print("Yetersiz Bakiye...")
            return
        else:
            self.bakiye -= cekilen_tutar
            self.islem_gecmisi.append(f"{datetime.now()} – Hesabınızdan {cekilen_tutar} TL çekildi")
            print(f"{cekilen_tutar} TL başarıyla çekildi. Güncel bakiye: {self.bakiye} TL")

    def __add__(self,other):
        return self.bakiye+other.bakiye

    def hesap_raporu(self):
        print("--- Hesap Raporu---")
        for islem in self.islem_gecmisi:
            print(islem)

def main():
    print("=== Banka Hesap Sistemi Test ===")

    # Hesap oluşturma
    hesap1 = BankaHesabi("12345", 1000, "Vadesiz", datetime.now())
    hesap2 = BankaHesabi("67890", 500, "Vadeli", datetime.now())

    print("\n--- Hesap Bilgileri ---")
    print(hesap1)
    print(hesap2)

    # İşlemler
    print("\n--- İşlemler ---")
    hesap1.para_yatir(500)
    hesap1.para_cek(200)
    hesap1.para_cek(2000)  # yetersiz bakiye örneği

    # Rapor
    print("\n--- Hesap 1 Raporu ---")
    hesap1.hesap_raporu()

    # __add__ test
    toplam_bakiye = hesap1 + hesap2
    print(f"\nToplam bakiye: {toplam_bakiye} TL")


if __name__ == "__main__":
    main()

