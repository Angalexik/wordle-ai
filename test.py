from solver import WORDLE_ANSWERS_WORDLIST, Score, Solver
from multiprocessing import Pool
from random import shuffle

# Starting wordle words:
# "adieu": 3.714 2%
# "oater": 3.550 0%
# "soare": 3.580 0%
# "crate": 3.430 0%
# "tweak": 3.808 1%
# "irate": 3.550 0%

# Starting squabble words:
# "adieu": 3.357 1%
# "oater": 3.576 1%
# "soare": 3.364 1%
# "crate": 3.404 1%
# "tweak": 3.606 1%
# "irate": 3.420 0%

AMOUNT = 100
shuffle(WORDLE_ANSWERS_WORDLIST, lambda: 0.4)  # random number chosen by rolling a dice

def test(start_word):
    amounts: list[int] = []
    failures: int = 0
    for answer in WORDLE_ANSWERS_WORDLIST[:AMOUNT]:
        guesses: list[str] = []

        def enter_word(word: str):
            guesses.append(word)

        def get_letter_score(word_num: int, letter_num: int) -> Score:
            # Too lazy to implement double letter words
            if guesses[word_num] == answer:
                return Score.CORRECT_POSITION
            # try:
            #     assert len(guesses[word_num]) == len(set(guesses[word_num]))
            # except:
            #     print(f"guess: {guesses[word_num]} answer: {answer}")
            #     raise NotImplementedError

            letter = guesses[word_num][letter_num]
            if answer[letter_num] == letter:
                return Score.CORRECT_POSITION
            if letter in answer:
                return Score.INCORRECT_POSITION
            return Score.NOT_IN_WORD

        solver = Solver(enter_word, get_letter_score, start_word)
        tries = solver.solve()
        if tries > 6:
            failures += 1
        else:
            amounts.append(tries)

    print(f"--------------\nAverage number of guesses:\n{sum(amounts) / len(amounts)}\nFailure rate:\n{failures / AMOUNT * 100}%\n{start_word}\n--------------\n")

start_words = ["slate", "oater", "roate", "soare", "crate", "salet", "reast", "crane", "trace"]
# start_words = ["oater"]

with Pool(6) as p:
    p.map(test, start_words)
# for start_word in ["irate", "oater", "adieu", "soare", "crate", "tweak"]:
