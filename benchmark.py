from solver_lib import Solver, Score
import json
import timeit
import time

WORDLE_ANSWERS_WORDLIST: list[str] = json.load(open("wordle_answer_words.json"))
WORDLE_GUESS_WORDLIST: list[str] = json.load(open("wordle_guess_words.json"))
WORDLE_WORDLIST = list(set(WORDLE_ANSWERS_WORDLIST + WORDLE_GUESS_WORDLIST))

guesses: list[str] = []
the_word = "cynic"

def enter_word(word: str):
    guesses.append(word)

def get_word_score(guess: str, answer: str) -> list[Score]:
    if guess == answer:
        return [Score.CORRECT_POSITION] * 5

    score = []
    for i, letter in enumerate(guess):
        if answer[i] == letter:
            score.append(Score.CORRECT_POSITION)
        elif letter in answer:
            score.append(Score.INCORRECT_POSITION)
        else:
            score.append(Score.NOT_IN_WORD)
    return score

def get_score() -> list[list[Score]]:
    return [get_word_score(w, the_word) for w in guesses]

solver = Solver(enter_word, get_score, WORDLE_ANSWERS_WORDLIST, WORDLE_WORDLIST, "crate")
start_time = time.perf_counter()
solver.solve()
guesses = []
solver.reset()
solver.solve()
# print(6000 * (time.perf_counter() - start_time))
# timeit.timeit(stmt="solver.solve()", setup="solver.reset()\nguesses = []", globals=globals(), number=6000)
