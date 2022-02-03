import json
import re

# with open("dictionary.txt", "r") as dictionary:
#     words = [w.lower() for w in [w[:-1] for w in dictionary.readlines()] if len(w) == 5]
#     with open("ott_guess_words.json", "+w") as guess_words:
#         guess_words.write(json.dumps(words))

guesses = json.load(open("ott_guess_words.json", "r"))
answers = json.load(open("ott_answer_words.json", "r"))

print(json.dumps([w for w in answers if w in guesses]))
