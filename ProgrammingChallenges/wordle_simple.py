# [$]> python3 wordle_simple.py

import random

GREEN = 'green'
YELLOW = 'yellow'
GREY = 'grey'
WORD_LEN = 5
NUM_TRIES = 15
DICT_FILE = './data/words.txt'
MATCHING_SCORE = [GREEN] * WORD_LEN

def main():
  word_list = get_word_list()
  solution = random.choice(word_list)
  guesses = []
  scores = []

  print('solution:', solution)

  while not scores or (scores[-1] != MATCHING_SCORE and len(guesses) < NUM_TRIES):
    guesses.append(random.choice(word_list))
    print('guesses:', guesses)
    scores.append(score_word(solution=solution, guess=guesses[-1]))
    print('score:', scores[-1])
    word_list = prune_words(word_list, guesses, scores)

  if solution == guesses[-1]:
    print(f'guessed solution in {len(guesses)} attempts')
  else:
    print(f'failed to guess solution after {NUM_TRIES} attempts')

def get_word_list() -> list[str]:
  word_list = []

  with open(DICT_FILE) as dict_file:
    for line in dict_file:
      clean_line = line.strip()
      if len(clean_line) == WORD_LEN:
        word_list.append(clean_line)

  return word_list

def prune_words(word_list, guesses, scores) -> list[str]:
  words = []

  grey_letters = set()
  yellow_letters = set()
  for i, guess in enumerate(guesses):
    grey_letters.update(get_matching_letters(guess, scores[i], GREY))
    yellow_letters.update(get_matching_letters(guess, scores[i], YELLOW))

  for word in word_list:
    if word not in guesses and has_matching_letters(word, guesses[-1], scores[-1]):
      if all(yellow_letter in word for yellow_letter in yellow_letters):
        if not any(grey_letter in word for grey_letter in grey_letters):
          words.append(word)

  return words

def get_matching_indexes(arr, color) -> list[int]:
  return [i for i, x in enumerate(arr) if x == color]

def get_matching_letters(word, arr, color) -> list[str]:
  letter_indexes = get_matching_indexes(arr, color)
  return [x for i, x in enumerate(word) if i in letter_indexes]

def has_matching_letters(word, guess, score) -> bool:
  matching_indexes = get_matching_indexes(score, GREEN)

  matching_count = 0
  for matching_index in matching_indexes:
    if word[matching_index] == guess[matching_index]:
      matching_count += 1

  return matching_count == len(matching_indexes)

def score_word(solution: str, guess: str) -> list[str]:
  """
  Assume the solution and the guess are five letters long.

  Returns: a list of colors, one for each letter, so len = 5.

  e.g. ['grey', 'green', 'yellow', 'grey', 'grey']

  - A color of "green" means that the letter matched in the right position
  - A color of "yellow" means that the letter matched but was in the wrong position
  - Everything else is "grey"
  """

  result = []

  for index, letter in enumerate(solution):
    if letter == guess[index]:
      result.append(GREEN)
    elif guess[index] in solution:
      result.append(YELLOW)
    else:
      result.append(GREY)

  # TODO: Handle Keeping Track Of Yellow Letters (Letters Can't Be Reused)

  return result

assert has_matching_letters('rugby', 'rurlz', [GREEN, GREEN, GREY, GREY, GREEN]) == False
assert has_matching_letters('rugby', 'rurly', [GREEN, GREEN, GREY, GREY, GREEN]) == True

assert score_word(solution='zzzzz', guess='aaaaa') == [GREY, GREY, GREY, GREY, GREY]
# assert score_word(solution='bozos', guess='roomy') == [GREY, GREEN, GREY, GREY, GREY]
# assert score_word(solution='bones', guess='roomy') == [GREEN, GREEN, GREY, GREY, GREY]
assert score_word(solution='hello', guess='hello') == [GREEN, GREEN, GREEN, GREEN, GREEN]
# assert score_word(solution='rugby', guess='rurly') == [GREEN, GREEN, GREY, GREY, GREEN]
# assert score_word(solution='ruger', guess='rurry') == [GREEN, GREEN, YELLOW, GREY, GREY]

main()
