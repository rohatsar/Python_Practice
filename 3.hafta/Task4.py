import math
# Kullanıcıdan bir sayı girmesini isteyen ve bu sayının karekökünü hesaplayan bir program yazın.
# - Negatif sayı girilirse uygun hata mesajı verin
# - Sayı yerine metin girilirse uygun hata mesajı verin
# - Try-except blokları kullanın
# - Geri bildirime göre: Hatalı giriş (metin veya negatif) durumunda tekrar giriş isteyin.
# - Kullanıcı "quit" yazarak çıkabilsin.

while True:
    user_input = input("Please enter a number (or 'quit' to exit): ")

    # 1. Çıkış kontrolü
    if user_input.lower() == 'quit':
        print("Exiting the program.")
        break

    # 2. Giriş işleme
    try:
        number = float(user_input)  # Hem tam sayı hem de ondalıklı girişi kapsar
        
        # 3. Negatif sayı kontrolü
        if number >= 0:
            sqrt_number = math.sqrt(number)
            print(f"The square root of {number} is {sqrt_number:.2f}")
            break  # Başarılı işlem, döngüyü sonlandır
        else:
            # Hata: Negatif sayı. Döngü devam edecek (break çalışmayacak)
            print("Error: Negative numbers are not allowed! Please try again.")

    # 4. Geçersiz tip (metin) kontrolü
    except ValueError:
        # Hata: Metin girişi. Döngü devam edecek
        print("Error: Invalid input! Please enter a valid number (e.g., 16 or 25.5).")