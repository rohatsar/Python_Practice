numbers=[1,2,3,4,5,6,7,8,9,10]
squares=[]

for number in numbers:
   number = number **2 #pow(number,2) de olabilir
   squares.append(number)

print(f"{'Number':<6} {'Square':<6}")
print("----------------")
for number in numbers:
    print(f"{number:<6} {number**2:<6}")