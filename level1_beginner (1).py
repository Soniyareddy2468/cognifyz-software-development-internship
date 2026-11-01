"""
Cognifyz Software Development Internship - Level 1: Beginner
Task 1: Basic text-based game (number guessing)
Task 2: Generate and print simple number patterns
"""

import random


# ---------------------------------------------------------------- Task 1
def guessing_game():
    """Number guessing game driven by conditional statements."""
    print("\n=== NUMBER GUESSING GAME ===")
    print("Choose difficulty: 1) Easy (1-10, 5 tries)  2) Medium (1-50, 7 tries)  3) Hard (1-100, 7 tries)")
    choice = input("Your choice (1/2/3): ").strip()

    if choice == "1":
        low, high, tries = 1, 10, 5
    elif choice == "2":
        low, high, tries = 1, 50, 7
    elif choice == "3":
        low, high, tries = 1, 100, 7
    else:
        print("Invalid choice, defaulting to Medium.")
        low, high, tries = 1, 50, 7

    secret = random.randint(low, high)
    print(f"I'm thinking of a number between {low} and {high}. You have {tries} tries.")

    for attempt in range(1, tries + 1):
        raw = input(f"Attempt {attempt}/{tries} - your guess: ").strip()
        if not raw.lstrip("-").isdigit():
            print("Please enter a whole number.")
            continue
        guess = int(raw)

        if guess < low or guess > high:
            print(f"Out of range! Stay between {low} and {high}.")
        elif guess == secret:
            print(f"Correct! You got it in {attempt} attempt(s).")
            return
        elif guess < secret:
            print("Too low.")
        else:
            print("Too high.")

    print(f"Game over! The number was {secret}.")


# ---------------------------------------------------------------- Task 2
def pyramid(n):
    """1 / 1 2 / 1 2 3 ... centred pyramid."""
    for i in range(1, n + 1):
        print(" " * (n - i) + " ".join(str(j) for j in range(1, i + 1)))


def right_triangle(n):
    for i in range(1, n + 1):
        print(" ".join(str(j) for j in range(1, i + 1)))


def inverted_triangle(n):
    for i in range(n, 0, -1):
        print(" ".join(str(j) for j in range(1, i + 1)))


def floyd_triangle(n):
    num = 1
    for i in range(1, n + 1):
        row = []
        for _ in range(i):
            row.append(str(num))
            num += 1
        print(" ".join(row))


def diamond(n):
    for i in range(1, n + 1):
        print(" " * (n - i) + " ".join(str(j) for j in range(1, i + 1)))
    for i in range(n - 1, 0, -1):
        print(" " * (n - i) + " ".join(str(j) for j in range(1, i + 1)))


def number_patterns():
    print("\n=== NUMBER PATTERNS ===")
    patterns = {
        "1": ("Pyramid", pyramid),
        "2": ("Right triangle", right_triangle),
        "3": ("Inverted triangle", inverted_triangle),
        "4": ("Floyd's triangle", floyd_triangle),
        "5": ("Diamond", diamond),
    }
    for key, (name, _) in patterns.items():
        print(f"{key}) {name}")
    choice = input("Select pattern: ").strip()
    if choice not in patterns:
        print("Invalid pattern.")
        return
    raw = input("Number of rows (1-20): ").strip()
    if not raw.isdigit() or not 1 <= int(raw) <= 20:
        print("Please enter a number between 1 and 20.")
        return
    print()
    patterns[choice][1](int(raw))


# ---------------------------------------------------------------- Menu
def main():
    while True:
        print("\n--- LEVEL 1 MENU ---")
        print("1) Guessing game (Task 1)")
        print("2) Number patterns (Task 2)")
        print("0) Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            guessing_game()
        elif choice == "2":
            number_patterns()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
