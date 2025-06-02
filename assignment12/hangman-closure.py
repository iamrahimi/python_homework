def make_hangman(secret_word):
    guesses = []

    def hangman_closure(letter):
        guesses.append(letter.lower())
        displayed = ''
        for char in secret_word:
            if char.lower() in guesses:
                displayed += char
            else:
                displayed += '_'
        print("Current word:", displayed)
        return all(char.lower() in guesses for char in secret_word)

    return hangman_closure


# --- Main game logic ---
def main():
    secret_word = input("Enter the secret word: ")
    print("\n" * 50)  # Clear the screen for secrecy

    hangman = make_hangman(secret_word)

    while True:
        guess = input("Guess a letter: ").strip()
        if not guess or len(guess) != 1 or not guess.isalpha():
            print("Please enter a single alphabetical character.")
            continue

        if hangman(guess):
            print(f"Congratulations! You guessed the word: {secret_word}")
            break


if __name__ == "__main__":
    main()