sum_odd = 0

for i in range(10):
    number = int(input(f"Please enter number {i + 1} of 10: \n"))

    if number % 2 != 0:
        sum_odd += number
        print(f"Added {number} to the total.")
    else:
        print(f"{number} is even, skipped.")

    print(f"You have {10 - (i + 1)} numbers left.\n")

print(f"The sum of your odd numbers is: {sum_odd}")