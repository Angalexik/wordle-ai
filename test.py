from solver import Score, Solver
from multiprocessing import Pool
import random
from PIL import Image

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
# random.seed(4)  # random number chosen by rolling a dice
# random.shuffle(WORDLE_ANSWERS_WORDLIST)
# print(WORDLE_ANSWERS_WORDLIST[:100])
best_words = [  # i have the best words
    "spell",
    "tulip",
    "brock",
    "bliss",
    "turbo",
    "polls",
    "began",
    "blast",
    "wheel",
    "troop",
    "mixes",
    "royal",
    "rocky",
    "grave",
    "kelly",
    "jones",
    "usage",
    "septa",
    "snack",
    "pasha",
    "combo",
    "glory",
    "gains",
    "scope",
    "likes",
    "voice",
    "karma",
    "types",
    "shawn",
    "windy",
    "creek",
    "fanny",
    "seems",
    "jumps",
    "clans",
    "takes",
    "twins",
    "study",
    "sandy",
    "loses",
    "laird",
    "cover",
    "lacks",
    "buyer",
    "piers",
    "later",
    "earls",
    "cache",
    "swans",
    "seine",
    "salts",
    "ducks",
    "gates",
    "rolls",
    "thing",
    "snoop",
    "burns",
    "waves",
    "foley",
    "awake",
    "serve",
    "papal",
    "dying",
    "triad",
    "alive",
    "would",
    "nasal",
    "taped",
    "rough",
    "among",
    "dream",
    "dress",
    "coupe",
    "helix",
    "facts",
    "duets",
    "halls",
    "marry",
    "slide",
    "vicar",
    "chaos",
    "trial",
    "nerve",
    "stoke",
    "males",
    "trail",
    "heron",
    "psalm",
    "nexus",
    "uncle",
    "lasts",
    "valor",
    "tough",
    "baker",
    "dusky",
    "bikes",
    "nails",
    "baton",
    "sails",
    "guide",
]


def test(start_word):
    amounts: list[int] = []
    failures: int = 0
    for answer in best_words:
        guesses: list[str] = []

        def enter_word(word: str):
            guesses.append(word)

        def get_letter_score(word_num: int, letter_num: int, _) -> Score:
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

        solver = Solver(
            enter_word, get_letter_score, lambda: Image.new("L", (5, 5)), start_word
        )
        tries = solver.solve()
        if tries > 6:
            failures += 1
        else:
            amounts.append(tries)

    print(
        f"--------------\nAverage number of guesses:\n{sum(amounts) / len(amounts)}\nFailure rate:\n{failures / AMOUNT * 100}%\n{start_word}\n--------------\n"
    )


start_words = [
    "dares",
    "arden",
    "slate",
    "roate",
    "soare",
    "crate",
    "salet",
    "reast",
]
# start_words = ["oater"]

# test("crate")
test("slate")

# with Pool(6) as p:
#     p.map(test, start_words)
# for start_word in ["irate", "oater", "adieu", "soare", "crate", "tweak"]:
