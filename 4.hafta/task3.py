import random
import os
import string
import re
import shutil
# Dosya Yöneticisi ( File Operations + Random)
# Dosya ve klasör işlemleri için kapsamlı bir yönetici sınıfı.
# Dosya oluşturma, okuma, arama ve yedekleme işlemleri yapabilmeli.
# dosya_olustur methodu: random modülü ile rastgele isimli dosya oluşturacak.
# dosya_oku_regex methodu: re modülü ile dosya içinde pattern arayacak
# klasör_tarama methodu: os modülü ile belirtilen klasördeki tüm dosyaları listeleyecek.
# __len__ methodu: klasördeki dosya sayısını döndürecek.

class DosyaYoneticisi:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def dosya_olustur(self):
        """Random isimli boş bir dosya oluşturur"""
        dosya_adi = ''.join(random.choices(string.ascii_letters + string.digits, k=8)) + ".txt"
        dosya_yolu = os.path.join(self.folder_path, dosya_adi)

        with open(dosya_yolu, "w") as f:
            f.write("")  # boş içerik

        print(f"✅ Dosya başarıyla oluşturuldu: {dosya_adi}")
        return dosya_adi

    def dosya_oku_regex(self, dosya_adi, pattern):
        """Belirtilen dosyada regex pattern'ine uyan ifadeleri bulur"""
        dosya_yolu = os.path.join(self.folder_path, dosya_adi)

        if not os.path.exists(dosya_yolu):
            print("❌ Dosya bulunamadı.")
            return []

        with open(dosya_yolu, "r") as f:
            icerik = f.read()

        eslesmeler = re.findall(pattern, icerik)
        if eslesmeler:
            print(f"🔍 Bulunan eşleşmeler: {eslesmeler}")
        else:
            print("⚠️ Eşleşme bulunamadı.")
        return eslesmeler

    def klasor_tarama(self):
        """Klasördeki tüm dosyaları listeler"""
        dosyalar = os.listdir(self.folder_path)
        print(f"📂 {self.folder_path} içindeki dosyalar: {dosyalar}")
        return dosyalar

    def __len__(self):
        """Klasördeki dosya sayısını döndürür"""
        return len(os.listdir(self.folder_path))

    def dosya_yedekle(self, dosya_adi, yedek_klasoru):
        """Dosyayı belirtilen klasöre yedekler"""
        kaynak_yol = os.path.join(self.folder_path, dosya_adi)
        hedef_yol = os.path.join(yedek_klasoru, dosya_adi)

        if not os.path.exists(kaynak_yol):
            print(f"❌ {dosya_adi} bulunamadı!")
            return

        if not os.path.exists(yedek_klasoru):
            os.makedirs(yedek_klasoru)

        shutil.copy2(kaynak_yol, hedef_yol)
        print(f"✅ {dosya_adi}, {yedek_klasoru} klasörüne yedeklendi.")


def main():
    # Test klasörü
    ana_klasor = "test_klasor"
    yedek_klasor = "yedekler"

    # Klasör yoksa oluştur
    if not os.path.exists(ana_klasor):
        os.makedirs(ana_klasor)

    yonetici = DosyaYoneticisi(ana_klasor)

    # 1 - Rastgele dosya oluştur
    dosya_adi = yonetici.dosya_olustur()

    # 2 - Dosyaya biraz içerik yazalım (regex test etmek için)
    with open(os.path.join(ana_klasor, dosya_adi), "w") as f:
        f.write("Hello123 World456 TestABC 789 helloHELLO testTest")

    # 3 - Regex ile arama yapalım
    pattern = r"[A-Za-z]+[0-9]+"   # harf + sayı patterni örneği
    yonetici.dosya_oku_regex(dosya_adi, pattern)

    # 4 - Klasörü tara
    yonetici.klasor_tarama()

    # 5 - Dosya sayısını göster (__len__)
    print(f"Klasördeki dosya sayısı: {len(yonetici)}")

    # 6 - Dosyayı yedekle
    yonetici.dosya_yedekle(dosya_adi, yedek_klasor)


if __name__ == "__main__":
    main()

