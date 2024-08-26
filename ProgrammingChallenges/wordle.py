import random
import sys

# USAGE: use default params (word length of 5 with 6 tries)
# [$]> python3 wordle.py

# USAGE: python3 wordle.py [WORD_LEN] [NUM_TRIES]
# [$]> python3 wordle.py 6 10

GREEN = 'green'
YELLOW = 'yellow'
GREY = 'grey'
WORD_LEN = int(sys.argv[1]) if len(sys.argv) == 3 else 5
NUM_TRIES = int(sys.argv[2]) if len(sys.argv) == 3 else 6
DICT_FILE = './data/words.txt'
MATCHING_SCORE = [GREEN] * WORD_LEN

class Wordle():
  def __init__(self, dict_file, word_len, num_tries):
    self.word_len = word_len
    self.num_tries = num_tries
    self.words = self.__get_word_list(dict_file)
    self.word_list = self.__filter_word_list()
    self.solution = random.choice(self.word_list)
    self.guesses = []
    self.scores = []

  def __get_word_list(self, file) -> list[str]:
    with open(file) as f:
      return [line.rstrip('\n') for line in f]

  def __filter_word_list(self) -> list[str]:
    return [word for word in self.words if len(word) == self.word_len]

  def run(self):
    print('solution:', self.solution)

    while not self.scores or (self.scores[-1] != MATCHING_SCORE and len(self.guesses) < self.num_tries):
      self.guesses.append(random.choice(self.word_list))
      print('guesses:', self.guesses)
      self.scores.append(self.score_guess())
      print('score:', self.scores[-1])
      self.word_list = self.prune_words()

    if self.solution == self.guesses[-1]:
      print(f'guessed solution in {len(self.guesses)} attempts')
    else:
      print(f'failed to guess solution after {NUM_TRIES} attempts')

  def prune_words(self) -> list[str]:
    words = []
    score = self.scores[-1]

    grey_letters = set()
    yellow_letters = set()
    for i, guess in enumerate(self.guesses):
      grey_letters.update(self.get_matching_letters(guess, self.scores[i], GREY))
      yellow_letters.update(self.get_matching_letters(guess, self.scores[i], YELLOW))

    for word in self.word_list:
      if word not in self.guesses and self.has_matching_letters(word, self.guesses[-1], score):
        if all(yellow_letter in word for yellow_letter in yellow_letters):
          if not any(grey_letter in word for grey_letter in grey_letters):
            words.append(word)

    return words

  def get_matching_indexes(self, arr, color) -> list[int]:
    return [i for i, x in enumerate(arr) if x == color]

  def get_matching_letters(self, word, arr, color) -> list[str]:
    letter_indexes = self.get_matching_indexes(arr, color)
    return [x for i, x in enumerate(word) if i in letter_indexes]

  def has_matching_letters(self, word, guess, score) -> bool:
    matching_indexes = self.get_matching_indexes(score, GREEN)

    matching_count = 0
    for matching_index in matching_indexes:
      if word[matching_index] == guess[matching_index]:
        matching_count += 1

    return matching_count == len(matching_indexes)

  def score_guess(self) -> list[str]:
    """
    Assume the solution and the guess are five letters long.

    Returns: a list of colors, one for each letter, so len = 5.

    e.g. ['grey', 'green', 'yellow', 'grey', 'grey']

    - A color of "green" means that the letter matched in the right position
    - A color of "yellow" means that the letter matched but was in the wrong position
    - Everything else is "grey"
    """

    result = []
    guess = self.guesses[-1]

    for index, letter in enumerate(self.solution):
      if letter == guess[index]:
        result.append(GREEN)
      elif guess[index] in self.solution:
        result.append(YELLOW)
      else:
        result.append(GREY)

    # TODO: Handle Keeping Track Of Yellow Letters (Letters Can't Be Reused)

    return result

wordle = Wordle(DICT_FILE, WORD_LEN, NUM_TRIES)
wordle.run()
