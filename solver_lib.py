from collections import Counter
from enum import Enum, auto
from functools import cmp_to_key
from time import time, sleep
from typing import Callable
from string import ascii_lowercase


class Score(Enum):
    NOT_IN_WORD = 0
    CORRECT_POSITION = 2
    INCORRECT_POSITION = 1
    UNKNOWN = 99


class Solver:
    def __init__(
        self,
        enter_word: Callable[[str], None],
        get_scores: Callable[[], list[list[Score]]],
        answer_words: list[str],
        wordlist: list[str],
        start_word=None,
    ):
        self._original_answer_words = answer_words

        self.answer_words = answer_words
        self.frequencies: dict[str, int] = {}
        self.letter_blacklist: set[str] = set()
        self.letters_in_word: set[str] = set()
        self.known_positions: list[tuple[str, int]] = []
        self.letter_pos_blacklist: list[tuple[str, int]] = []
        self.unknown_letters: set[str] = set(ascii_lowercase)
        self.enter_word = enter_word
        self.get_scores = get_scores
        self.start_word = start_word

        self.update_frequencies()
        self._original_frequencies = self.frequencies
        self._original_wordlist = self.sort_wordlist(wordlist)
        self.test_words = self._original_wordlist

    def reset(self):
        # print("resetting")
        # print(f"All known positions: {self.known_positions}")
        # print(f"All possible answers: {self.answer_words}")
        # print(f"All possible words for testing: {self.test_words}")
        # sleep(0.5)
        self.answer_words = self._original_answer_words
        self.test_words = self._original_wordlist
        self.frequencies: dict[str, int] = self._original_frequencies
        self.letter_blacklist: set[str] = set()
        self.letters_in_word: set[str] = set()
        self.known_positions: list[tuple[str, int]] = []
        self.letter_pos_blacklist: list[tuple[str, int]] = []
        self.unknown_letters: set[str] = set(ascii_lowercase)


        # self.__init__(
        #     self.enter_word,
        #     self.get_scores,
        #     self._original_answer_words,
        #     self._original_wordlist,
        #     self.start_word,
        # )

    def update_frequencies(self):
        self.frequencies = dict(Counter("".join(self.answer_words)))
        # self.frequencies = { k:v for (k,v) in zip(self.frequencies.keys(), self.frequencies.values()) if k in self.unknown_letters }
        for letter in ascii_lowercase:
            if letter not in self.frequencies:
                self.frequencies[letter] = 0
        # for word in self.answer_words:
        #     for (idx, letter) in enumerate(word):
        #         self.frequencies[letter][idx] += 1

    def sort_wordlist(self, wordlist: list[str]) -> list[str]:
        def compare_words(word1: str, word2: str) -> int:
            def letter_val(args: tuple[int, str]):
                # args[0]: index of the letter in the word
                # args[1]: the letter
                return self.frequencies[args[1]]

            first_value = sum(map(letter_val, enumerate(set(word1))))
            second_value = sum(map(letter_val, enumerate(set(word2))))

            if first_value < second_value:
                return -1
            if first_value > second_value:
                return 1
            return 0

        return sorted(wordlist, key=cmp_to_key(compare_words), reverse=True)

    def filter_wordlist(self, wordlist: list[str], current_word: str) -> list[str]:
        def filter_function(word: str) -> bool:
            if word == current_word:
                return False
            for letter in self.letter_blacklist:
                if letter in word:
                    return False
            for letter in self.letters_in_word:
                if letter not in word:
                    return False
            for (letter, pos) in self.letter_pos_blacklist:
                if word[pos] == letter:
                    return False
            for (letter, pos) in self.known_positions:
                if word[pos] != letter:
                    return False
            return True

        return [x for x in wordlist if filter_function(x)]
        # return list(filter(filter_function, wordlist))

    def guess_word(self, word: str, word_num: int) -> bool:  # returns true if it reset
        self.enter_word(word)
        scores = self.get_scores()

        try:
            if scores == [] or scores[0][0] == Score.UNKNOWN or all([s == Score.CORRECT_POSITION for s in scores[word_num]]):
                self.reset()
                return True
        except:
            self.reset()
            return True

        for position, letter in enumerate(word):
            score = scores[word_num][position]
            if score == Score.NOT_IN_WORD:
                self.letter_blacklist.add(letter)
            elif score == Score.INCORRECT_POSITION:
                self.letters_in_word.add(letter)
                self.letter_pos_blacklist.append((letter, position))
            elif score == Score.CORRECT_POSITION:
                self.known_positions.append((letter, position))

        self.letter_blacklist -= self.letters_in_word | set(
            [x[0] for x in self.known_positions]
        )

        # print(self.test_words)

        self.answer_words = self.filter_wordlist(self.answer_words, word)
        if len(self.answer_words) == 0:
            self.reset()
            return True
        self.update_frequencies()
        self.test_words = self.sort_wordlist(
            self.filter_wordlist(self.test_words, word)
        )
        return False

    def solve_forever(self, condition: Callable[[], bool]):
        while condition():
            self.solve()

    def solve(self) -> int:
        for i in range(6):
            try:
                if self.start_word:
                    word = self.start_word if i == 0 else self.test_words[0]
                else:
                    word = self.test_words[0]
            except IndexError:
                return i
            if len(self.answer_words) <= 2:
                word = self.answer_words[0]
            if self.guess_word(word, i):
                # print(f"Can't believe I got it in only {i + 1} guesses")
                return i + 1
        self.reset()
        return 99
