import json
import random
from typing import List, Tuple
from time import sleep
from functools import cmp_to_key
from collections import Counter

import pyautogui
from PIL import ImageGrab

ANSWERS_WORDLIST: List[str] = json.load(open('answer_words.json'))
GUESS_WORDLIST: List[str]

SCORES_COLOUR_TABLE = {
    (58, 58, 60): 'not_in_word',
    (83, 141, 78): 'correct_position',
    (181, 159, 59): 'incorrect_position',
    (18, 18, 19): 'unknown',
}

frequencies = json.load(open('letter_frequencies.json', 'r', encoding='utf8'))


def compare(first: str, second: str) -> int:
    if len(set(first)) != len(first):
        return -1
    if len(set(second)) != len(second):
        return 1

    first_value = sum(map(lambda c: frequencies[c.upper()], list(first)))
    second_value = sum(map(lambda c: frequencies[c.upper()], list(second)))

    if first_value < second_value:
        return -1
    if first_value > second_value:
        return 1
    return 0


with open('guess_words.json', 'r', encoding="utf8") as file:
    GUESS_WORDLIST = json.load(file)
    unique_letters = list(filter(lambda w: len(set(w)) == len(w), GUESS_WORDLIST))
    same_letters = list(filter(lambda w: len(set(w)) != len(w), GUESS_WORDLIST))
    # random.shuffle(unique_letters)
    # random.shuffle(same_letters)
    GUESS_WORDLIST = unique_letters + same_letters


def get_letter_score(word_num: int, letter_num: int) -> str:
    screen = ImageGrab.grab(bbox=(3795, 874, 3795 + 330, 874 + 400)) 
    score = screen.getpixel((2 + 67 * letter_num, 2 + 70 * word_num))
    print(score)
    return SCORES_COLOUR_TABLE[score]


def filter_wordlist(wordlist: List[str], current_word: str, known_positions: List[Tuple[str, int]], letters_in_word: List[str], letter_blacklist: List[str]):
    global frequencies

    def filter_function(word: str) -> bool:
        if word == current_word:
            return False
        for letter in letter_blacklist:
            if letter in word:
                return False
        for letter in letters_in_word:
            if letter not in word:
                return False
        for (letter, pos) in known_positions:
            if word[pos] != letter:
                return False
        return True

    filtered_list = list(filter(filter_function, wordlist))
    frequencies = dict(Counter(''.join(filtered_list).upper()))
    return sorted(filtered_list, key=cmp_to_key(compare), reverse=True)



def main():
    sleep(5)
    test_words = GUESS_WORDLIST + ANSWERS_WORDLIST
    guess_words = ANSWERS_WORDLIST
    letter_blacklist = []
    letters_in_word = []
    known_positions = []
    for i in range(6):
        word = test_words[0] if i != 0 else 'atone'
        if len(guess_words) <= 2:
            word = guess_words[0]
        pyautogui.typewrite(list(word) + ['enter'], interval=0.04)
        sleep(2)
        for position, letter in enumerate(word):
            score = get_letter_score(i, position)
            if score == 'not_in_word':
                letter_blacklist += letter
            elif score == 'incorrect_position':
                letters_in_word += letter
            elif score == 'correct_position':
                known_positions += [(letter, position)]

        test_words = filter_wordlist(test_words, word, known_positions, letters_in_word, letter_blacklist)
        guess_words = filter_wordlist(guess_words, word, known_positions, letters_in_word, letter_blacklist)
        print('knoll' in test_words)
        print('knoll' in guess_words)
        if not guess_words:
            print(f"Can't believe I got it in only {i + 1} guesses")
            break;


main()
