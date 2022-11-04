import random  # import to allow a random item to be picked
import maskpass  # import to allow an input message to be hidden
from werkzeug.security import check_password_hash
import sqlite3

db = sqlite3.connect('../instance/flaskr.sqlite')
# here a random word is chosen from a large word file.
with open('most_common_words.txt', 'r') as f:
    word_list = f.read().splitlines()

easy_dif = [word for word in word_list if len(
    word) <= 5 and " " not in word and str(range(0, 9)) not in word]
medium_dif = [word for word in word_list if len(word) >= 6 and len(
    word) <= 7 and " " not in word and str(range(0, 9)) not in word]
hard_dif = [word for word in word_list if len(
    word) >= 8 and " " not in word and str(range(0, 9)) not in word]

while True:  # 2 loops to allow the player to play again
    while True:
        attempts = 10

        while True:
            print("Please login to continue.")
            username = input("Username: ")
            password = maskpass.askpass(prompt="password: ", mask="_")
            user = db.execute(
                'SELECT * FROM user WHERE username = ?', (username,)
            ).fetchone()
            if user is None:
                print("Wrong username.")
                continue
            elif not check_password_hash(user[2], password):
                print("wrong password.")
                continue
            print(f"You are logged in as {user[1]}.")
            break

        print("\n1. Alone")
        print("2. With a friend")
        game_mode = input("Would you like to play alone or with a friend? ")
        game_mode = game_mode.lower()

        if game_mode == "1" or game_mode == "alone":
            print("\n1. Easy\n2. Medium\n3. Hard")
            difficulty = input("Please choose a difficulty: ")
            difficulty = difficulty.lower()
            if difficulty == "1" or difficulty == "easy":
                easy = 1
                medium = 0
                hard = 0
                multiplayer = 0
                print(
                    "\nYou are playing alone on easy difficulty.\nA random word has been picked for you.")
                word = random.choice(easy_dif)
                break
            elif difficulty == "2" or difficulty == "medium":
                easy = 0
                medium = 1
                hard = 0
                multiplayer = 0
                print(
                    "\nYou are playing alone on medium difficulty.\nA random word has been picked for you.")
                word = random.choice(medium_dif)
                break
            elif difficulty == "3" or difficulty == "hard":
                easy = 0
                medium = 0
                hard = 1
                multiplayer = 0
                print(
                    "\nYou are playing alone on hard difficulty.\nA random word has been picked for you.")
                word = random.choice(hard_dif)
                break
            else:
                print("\nPlease pick a valid game_mode!\n")
        elif game_mode == "2" or game_mode == "with a friend":
            easy = 0
            medium = 0
            hard = 0
            multiplayer = 1
            print("You have chosen to play with a friend.\nLook away while your friend picks a word and the amount of attempts.\n")
            word = maskpass.askpass(prompt="Please pick a word: ", mask="_")
            word = word.lower()

            # numeric = attempts.isnumeric()  # to check if the attempts are a number
            # if attempts != attempts.isnumeric():
            #     print("Please pick a valid number of attempts!")
            #     continue
            # turning the attemps into an integer so they can later be substracted
            while True:
                try:
                    attempts = input("Please choose the amount of attempts: ")
                    attempts = int(attempts)
                    break
                except ValueError:
                    print("Please pick a number!")
                    continue
            break
        else:
            print("\nPlease pick a valid game_mode!\n")
    guessed_chars = []  # list where all previously guessed character go into.
    # hidden_word = ["_"] * len(word) # at first hidden words was a list
    hidden_word = "_" * len(word)

    print(
        f"\nThe word you have to guess consists of {len(word)} characters.\nYou are allowed {attempts} guesses.\n")
    while attempts > 0:
        # displays the underscored with a space between them
        print(" ".join(hidden_word))
        guess = input("Pick a letter or guess the word: ")
        guess = guess.lower()
        if guess == word:
            lost = 0
            won = 1
            print("Congratulations! You have guessed the word!")
            break
        elif len(guess) != 1:
            print("Please pick a single character to guess.")
            continue
        elif guess == " ":
            print("That is not a valid option!")
            continue
        # if statement to check if the guess has already been chosen before
        if guess in guessed_chars:
            print(
                f"You have already picked {guess} before. Please pick another character.")
            continue
        # guessed_chars needs to be appended under the previous if statements, same goes for the attemps since else an attempt would be substracted for an invalid input.
        guessed_chars.append(guess)
        attempts -= 1
        index = 0  # index is here to pick the correct index in hidden_word and replace the underscore with the guess
        underscore = 0
        # at first had a for loop to find the guess in the hidden word. But turning it into a string is more efficient.
        # for char in word:
        #     if guess == char:
        #         hidden_word[index] = guess
        #     index += 1
        while index < len(word):
            index = word.find(guess, index)
            if index == -1:
                break
            hidden_word = hidden_word[:index] + guess + hidden_word[index + 1:]
            index += 1
        # to end the game when all characters are already chosen
        underscore = hidden_word.find("_")
        print(f"\nYou have {attempts} guesses remaining.")
        if underscore == -1:
            lost = 0
            won = 1
            print(f"\nCongratulations! You have guessed the word!\n{word}\n")
            break
        if attempts == 0:
            lost = 1
            won = 0
            print(
                f"\nYou are out of guesses. The word was: '{word}'.\nBetter luck next time!\n")

    db.execute(
        f'INSERT INTO games_played (user_id, won, lost, easy, medium, hard, multiplayer) VALUES ({user[0]}, {won}, {lost}, {easy}, {medium}, {hard}, {multiplayer})'
    )
    db.commit()

    print("1. Yes")
    print("2. No")
    # play_again = ""
    while True:
        play_again = input("Would you like to play again? ")
        play_again = play_again.lower()
        # play_again = play_again.lower()
        if play_again == "1" or play_again == "yes":
            break
        elif play_again == "2" or play_again == "no":
            exit()
        print("\nPlease pick a valid choice!\n")
