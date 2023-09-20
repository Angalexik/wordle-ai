import json
import re

guesses = []

with open("dictionary.txt", "r") as dictionary:
    guesses = [
        w.lower() for w in [w[:-1] for w in dictionary.readlines()] if len(w) == 5
    ]
    with open("ott_guess_words.json", "+w") as guess_words:
        guess_words.write(json.dumps(guesses))


with open("en_wikt_words_1000_5-8.txt", "r") as dictionary:
    answers = [
        w.lower()
        for w in [w.split(" ")[0] for w in dictionary.readlines()]
        if len(w) == 5
    ]
    answers = [w for w in answers if w in guesses]
    with open("ott_answer_words.json", "+w") as answer_words:
        answer_words.write(json.dumps(answers))

# guesses = json.load(open("ott_guess_words.json", "r"))
# answers = json.load(open("ott_answer_words.json", "r"))

# print(json.dumps([w for w in answers if w in guesses]))
