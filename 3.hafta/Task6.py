# Bir isim listesindeki tüm isimleri büyük harfe çeviren ve başına "Sayın " ekleyen bir program yazın.
# Örnek: ["ali", "ayşe", "mehmet"] → ["Sayın ALİ", "Sayın AYŞE", "Sayın MEHMET"]
# - Lambda ve map kullanın
# - Kullanıcıdan virgülle ayrılmış isimler alın
# - DÜZELTME: Boşlukları, sayıları ve geçersiz karakterleri filtrele

user_input = input("Enter names separated by commas: ")

# 1. Adım: Girdiyi virgüllerden ayır
# "ali, ayşe, 123, ,,mehmet!" -> ['ali', ' ayşe', ' 123', ' ', '', 'mehmet!']
names = user_input.split(",")

# 2. Adım (Düzeltme 1): map kullanarak her ismin başındaki/sonundaki boşlukları temizle
# -> ['ali', 'ayşe', '123', '', '', 'mehmet!']
stripped_names = map(lambda name: name.strip(), names)

# 3. Adım (Düzeltme 2 & 3): filter kullanarak sadece harflerden oluşan (sayı/sembol/boşluk içermeyen)
# ve boş olmayan isimleri tut.
# 'ali'.isalpha() -> True
# 'ayşe'.isalpha() -> True
# '123'.isalpha() -> False
# ''.isalpha() -> False
# 'mehmet!'.isalpha() -> False
# -> ['ali', 'ayşe']
valid_names = filter(lambda name: name.isalpha(), stripped_names)

# 4. Adım: Kalan geçerli isimleri formatla
# -> ['Sayın ALİ', 'Sayın AYŞE']
format_name = lambda name: "Sayın " + name.upper()
formatted_names = list(map(format_name, valid_names))

print(formatted_names)