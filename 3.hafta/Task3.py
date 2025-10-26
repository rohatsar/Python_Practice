import math
# Gerçek zamanlı veri işleme sistemi:
# Kullanıcıdan sürekli sayı girmesini isteyin
# Her girişte:
# Sayıyı bir stream'e ekleyin
# Son 5 sayının ortalamasını hesaplayın (moving average)
# Standart sapma hesaplayın
# Anomaly detection (3 sigma kuralı)
# 'quit' yazınca program sonlansın
# Gereksinimler:
# - Generator functions for stream processing
# - Map/reduce operations on sliding window
# - Lambda for statistical calculations
# - Try-except for invalid inputs
# - Functional state management (no global variables)
# Örnek:
# Input: 10, 12, 15, 11, 9, 100 (anomali), 13
# Output: MA: 11.4, Std: 2.1, Anomaly: 100 detected!
def stream():
    while True:
        user_input = input("Enter a number (or 'quit'): ")
        if user_input.lower() == 'quit':
            break
        try:
            number = float(user_input)
            yield number
        except ValueError:
            print("Invalid input, please enter a number or 'quit'.")

def process_stream(window_size=5):
    window = []
    for number in stream():
        window.append(number)
        if len(window) > window_size:
            window.pop(0)

        mean = sum(window) / len(window)
        variance = sum(map(lambda x: (x - mean) ** 2, window)) / len(window)
        std_dev = math.sqrt(variance)
        is_anomaly = abs(number - mean) > 3 * std_dev

        print(f"\nWindow: {window}")
        print(f"Moving Average: {mean:.2f}")
        print(f"Standard Deviation: {std_dev:.2f}")
        if is_anomaly:
            print(f"⚠️  Anomaly detected! {number} is out of 3σ range.")
        else:
            print(f"{number} is normal.")

if __name__ == "__main__":
    print("Real-time data processing system (type 'quit' to exit)")
    process_stream()