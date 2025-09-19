def make_hangman(secret_word):
    guesses = []

    def hangman_closure(letter):
        guesses.append(letter.lower())

        # Build display string
        display = ""
        for ch in secret_word.lower():
            if ch in guesses:
                display += ch
            else:
                display += "_"
        print(display)

        # Check if all letters guessed
        return all(ch in guesses for ch in secret_word.lower())

    return hangman_closure


if __name__ == "__main__":
    # Prompt for secret word
    secret = input("Enter the secret word: ").strip()

    game = make_hangman(secret)

    print("\nLet's play Hangman!\n")
    while True:
        guess = input("Enter a letter: ").strip().lower()

        if not guess.isalpha() or len(guess) != 1:
            print("Please enter a single letter.")
            continue

        if game(guess):
            print(f"Congratulations! You guessed the word '{secret}'.")
            break