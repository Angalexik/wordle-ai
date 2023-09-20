import json
from time import sleep, time
from functools import cmp_to_key
from collections import Counter
from PIL import ImageGrab, Image
from string import ascii_lowercase
from enum import Enum, auto
import pyautogui
from typing import Callable
from solver_lib import Solver, Score


# WORDLE_ANSWERS_WORDLIST: list[str] = json.load(open("wordle_answer_words.json"))
# WORDLE_GUESS_WORDLIST: list[str] = json.load(open("wordle_guess_words.json"))

WORDLE_SCORES_COLOUR_TABLE = {
    (58, 58, 60): Score.NOT_IN_WORD,
    (83, 141, 78): Score.CORRECT_POSITION,
    (181, 159, 59): Score.INCORRECT_POSITION,
    (18, 18, 19): Score.UNKNOWN,
}

WORDLE_ANSWERS_WORDLIST: list[str] = json.load(open("ott_answer_words.json"))
WORDLE_GUESS_WORDLIST: list[str] = json.load(open("ott_guess_words.json"))

OTT_SCORES_COLOUR_TABLE = {
    (155, 93, 247): Score.NOT_IN_WORD,
    (46, 216, 60): Score.CORRECT_POSITION,
    (214, 190, 0): Score.INCORRECT_POSITION,
    (167, 113, 248): Score.UNKNOWN,
}

WORDLE_WORDLIST = list(set(WORDLE_ANSWERS_WORDLIST + WORDLE_GUESS_WORDLIST))


def get_screen() -> Image.Image:
    return ImageGrab.grab(bbox=(3795, 874, 3795 + 330, 874 + 400))


def get_letter_score(word_num: int, letter_num: int, screen: Image.Image) -> Score:
    score = screen.getpixel((2 + 67 * letter_num, 2 + 70 * word_num))
    return WORDLE_SCORES_COLOUR_TABLE[score]


def enter_word(word: str):
    pyautogui.write(list(word) + ["enter"], interval=0.02)
    sleep(0.2)


def ott_get_scores() -> list[list[Score]]:
    image = ImageGrab.grab(bbox=(3783, 983, 3783 + 354, 983 + 426))
    image.save(f"screens/{int(time())}.png")
    scores = [[Score.UNKNOWN for _ in range(5)] for _ in range(6)]
    for word_num in range(6):
        for letter_num in range(5):
            score = image.getpixel((5 + 75 * letter_num, 5 + 73 * word_num))
            print(score)
            scores[word_num][letter_num] = OTT_SCORES_COLOUR_TABLE[score]
    return scores


if __name__ == "__main__":
    solver = Solver(
        enter_word, ott_get_scores, WORDLE_ANSWERS_WORDLIST, WORDLE_WORDLIST, "slate"
    )
    # solver = Solver(enter_word, get_letter_score, get_screen, "crate")
    sleep(2)
    print(f"Can't believe I got in only {solver.solve_forever(lambda: True)} guesses")
