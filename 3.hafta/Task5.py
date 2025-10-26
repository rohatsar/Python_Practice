import math
# Dört işlem yapan bir hesap makinesi fonksiyonu yazın.
# - Toplama, çıkarma, çarpma, bölme işlemleri
# - Kullanıcıdan işlem tipi ve sayıları input ile alın
# - Bölme işleminde sıfıra bölme hatasını try-except ile yakalayın
# - Geçersiz işlem girilirse uygun mesaj verin
# - Lambda ifadeleri kullanarak işlemleri tanımlayın
# - Geri bildirime göre: Tüm girişler (operatör VE sayılar) için doğrulama eklendi.

def calculator():
    add = lambda x, y: x + y
    subtract = lambda x, y: x - y
    multiply = lambda x, y: x * y
    divide = lambda x, y: x / y

    # --- 1. Operatör Girişini Doğrulama Döngüsü ---
    valid_operations = ['+', '-', '*', '/']
    while True:
        operation = input("Enter operation (+, -, *, /): ")
        if operation in valid_operations:
            break  # Geçerli operatör, döngüden çık
        else:
            # Geri bildirimde istenen uyarı:
            print("Invalid operation! Please enter one of +, -, *, /")
    
    # --- 2. Sayı Girişlerini Doğrulama Döngüsü ---
    # Operatör geçerliyse, şimdi sayıları iste
    while True:
        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            break  # Her iki giriş de sayıya dönüştürülebildi, döngüden çık
        except ValueError:
            print("Invalid input! Please enter valid numbers.")
            # Döngü devam eder ve sayıları tekrar sorar

    # --- 3. Hesaplama ---
    # Bu aşamada 'operation' geçerli VE 'num1', 'num2' float.
    # Sadece sıfıra bölme hatasını kontrol etmemiz gerekiyor.
    try:
        if operation == '+':
            result = add(num1, num2)
        elif operation == '-':
            result = subtract(num1, num2)
        elif operation == '*':
            result = multiply(num1, num2)
        elif operation == '/':
            result = divide(num1, num2) # Hata burada oluşabilir
        
        print(f"The result of {num1} {operation} {num2} is {result}")

    except ZeroDivisionError:
        print("Error: Cannot divide by zero!")


if __name__ == "__main__":
    calculator()