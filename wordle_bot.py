import json
from time import sleep, time
from solver_lib import Score, Solver
import pyautogui
from PIL import ImageGrab

WORDLE_ANSWERS_WORDLIST: list[str] = json.load(open("wordle_answer_words.json"))
WORDLE_GUESS_WORDLIST: list[str] = json.load(open("wordle_guess_words.json"))

WORDLE_WORDLIST = list(set(WORDLE_ANSWERS_WORDLIST + WORDLE_GUESS_WORDLIST))

WORDLE_SCORES_COLOUR_TABLE = {
    (58, 58, 60): Score.NOT_IN_WORD,
    (83, 141, 78): Score.CORRECT_POSITION,
    (181, 159, 59): Score.INCORRECT_POSITION,
    (18, 18, 19): Score.UNKNOWN,
}

def enter_word(word: str):
    pyautogui.write(list(word) + ["enter"], interval=0.05)
    sleep(2)


def get_scores() -> list[list[Score]]:
    image = ImageGrab.grab(bbox=(3795, 874, 3795 + 330, 874 + 400))
    image.save(f"screens/{int(time())}.png")
    scores = [[Score.UNKNOWN for _ in range(5)] for _ in range(6)]
    for word_num in range(6):
        for letter_num in range(5):
            score = image.getpixel((2 + 67 * letter_num, 5 + 70 * word_num))
            print(score)
            scores[word_num][letter_num] = WORDLE_SCORES_COLOUR_TABLE[score]
    return scores

solver = Solver(enter_word, get_scores, WORDLE_ANSWERS_WORDLIST, WORDLE_WORDLIST, "crate")
solver.solve()