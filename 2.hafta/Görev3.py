import random
secret_num=random.randint(1, 100)
guess_count =10
guessed =False
print("Welcome to the Number Guessing Game!\n")
while guess_count > 0:
    guess = int(input("Enter a number between 1 and 100: \n"))

    if guess == secret_num:
        print(f"🎉 Congratulations! You found the secret number = {secret_num}!")
        guessed=True
        break
    elif guess < secret_num:
        print("🔺 Too low! Try a bigger number.")
        guess_count -= 1
        print(f"You have {guess_count} guesses left.")
    elif guess > secret_num:
        print("🔻 Too high! Try a smaller number.")
        guess_count -= 1
        print(f"You have {guess_count} guesses left.")

if guessed == False:
    print(f"Game Over! The secret number was {secret_num}")