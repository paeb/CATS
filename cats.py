"""Typing test implementation"""
from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime
import string

# Contributors: Harry, Brandon

###########
# Phase 1 #
###########

# lambda is an anonymous function
# a higher order function means we can take a function as a parameter

def choose(paragraphs, select, k):
  """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
  paragraph returns True. If there are fewer than K such paragraphs, return
  the empty string.

  Arguments:
    paragraphs: a list of strings
    select: a function that returns True for paragraphs that can be selected
    k: an integer

  >>> ps = ['hi', 'how are you', 'fine']
  >>> s = lambda p: len(p) <= 4
  >>> choose(ps, s, 0)
  'hi'
  >>> choose(ps, s, 1)
  'fine'
  >>> choose(ps, s, 2)
  ''
  """
  # BEGIN PROBLEM 1
  filtered_paragraphs = list(filter(select,paragraphs)) # -> returns a list where we check each element in a list, ps, with a function s
  if (len(filtered_paragraphs) > k):
    return filtered_paragraphs[k]
  else:
    return ""
  # END PROBLEM 1

def about(topic):
  """Return a select function that returns whether
  a paragraph contains one of the words in TOPIC.

  Arguments:
    topic: a list of words related to a subject

  >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
  >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
  'Cute Dog!'
  >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
  'Nice pup.'
  """
  assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'

  # BEGIN PROBLEM 2

  def in_topic(paragraph):
    print("DEBUG: " + paragraph)
    paragraph = paragraph.split() # split the string into words
    for p_word in paragraph: # each word in paragraph
      print("DEBUG: " + p_word)
      p_word = remove_punctuation(p_word)
      for word in topic: # word
        if word.lower() == p_word.lower():
          return True
    return False
  return in_topic

  # END PROBLEM 2

def accuracy(typed, reference):
  """Return the accuracy (percentage of words typed correctly) of TYPED
  when compared to the prefix of REFERENCE that was typed.

  Arguments:
    typed: a string that may contain typos
    reference: a string without errors

  >>> accuracy('Cute Dog!', 'Cute Dog.')
  50.0
  >>> accuracy('A Cute Dog!', 'Cute Dog.')
  0.0
  >>> accuracy('cute Dog.', 'Cute Dog.')
  50.0
  >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
  50.0
  >>> accuracy('Cute', 'Cute Dog.')
  100.0
  >>> accuracy('', 'Cute Dog.')
  0.0
  >>> accuracy('', '')
  100.0
  """
  typed_words = split(typed)
  reference_words = split(reference)

  # BEGIN PROBLEM 3
  '''
  Rules:
  - Order matters ("a b c d" "b a c d" 50.0)
  - Capitalization matters ("Cat" "cat" 0.0)
  - A word must immediately be followed by the next in the list ("a b c d", "a d" 25.0)
  - Tabs don't count as words ("a b \tc" , "a b c" 100.0)
  - Punctuation matters ("cats.", "cats" 0.0) 
  - The words must be in the exact order they were in the reference ("a b c d", "b c d" 0.0)
  '''
  # These are counting variables for keeping track of how many are correct 
  # compared to the total words
  count = 0
  total = len(typed_words)
  # This is in order to make sure we don't return something divided by 0
  if total == 0:
    total = 1
  # Checks if the two are the same before running the rest
  if typed_words == reference_words:
    return 100.0
  # Loops through typed_words while checking that it's within the length og reference_words
  for i in range(len(typed_words)):
    if i < len(reference_words):
      if typed_words[i] == reference_words[i]:
        count += 1
  # returns the percentage of typed words that are correct
  return 100 * (count / total)

  # END PROBLEM 3


def wpm(typed, elapsed):
  """Return the words-per-minute (WPM) of the TYPED string.

  Arguments:
    typed: an entered string
    elapsed: an amount of time in seconds

  >>> wpm('hello friend hello buddy hello', 15)
  24.0
  >>> wpm('0123456789',60)
  2.0
  """
  assert elapsed > 0, 'Elapsed time must be positive'

  # BEGIN PROBLEM 4
  return float(len(typed) / 5 / elapsed) * 60
  # END PROBLEM 4

###########
# Phase 2 #
###########

def autocorrect(typed_word, word_list, diff_function, limit):
  """Returns the element of WORD_LIST that has the smallest difference
  from TYPED_WORD. Instead returns TYPED_WORD if that difference is greater
  than LIMIT.

  Arguments:
    typed_word: a string representing a word that may contain typos
    word_list: a list of strings representing reference words
    diff_function: a function quantifying the difference between two words
    limit: a number

  >>> ten_diff = lambda w1, w2, limit: 10 # Always returns 10
  >>> autocorrect("hwllo", ["butter", "hello", "potato"], ten_diff, 20)
  'butter'
  >>> first_diff = lambda w1, w2, limit: (1 if w1[0] != w2[0] else 0) # Checks for matching first char
  >>> autocorrect("tosting", ["testing", "asking", "fasting"], first_diff, 10)
  'testing'
  """
  # BEGIN PROBLEM 5

  wordDiffs = [] # list to hold the word differences
  for i in range(len(word_list)): # for every word in the word list
    wordDiffs.append((word_list[i], diff_function(typed_word, word_list[i], limit))) # add the word (in the word list) and its difference from the typed word
  closest = wordDiffs[0] # choose one of the differences to start
  for i in wordDiffs: # for each tuple in the list: (word, difference) pair
    if i[0] == typed_word: # if the word is the typed word, just return it
      return i[0]
    elif i[1] < closest[1]: # if this word is closer to the typed word
      closest = i # set the new closest word
  
  if closest[1] <= limit: # if the closest word is less than the limit
    return closest[0]
  else:
    return typed_word

  # END PROBLEM 5

def sphinx_swaps(start, goal, limit):
  """A diff function for autocorrect that determines how many letters
  in START need to be substituted to create GOAL, then adds the difference in
  their lengths and returns the result.

  Arguments:
    start: a starting word
    goal: a string representing a desired goal word
    limit: a number representing an upper bound on the number of chars that must change

  >>> big_limit = 10
  >>> sphinx_swaps("nice", "rice", big_limit)  # Substitute: n -> r
  1
  >>> sphinx_swaps("range", "rungs", big_limit)  # Substitute: a -> u, e -> s
  2
  >>> sphinx_swaps("pill", "pillage", big_limit) # Don't substitute anything, length difference of 3.
  3
  >>> sphinx_swaps("roses", "arose", big_limit)  # Substitute: r -> a, o -> r, s -> o, e -> s, s -> e
  5
  >>> sphinx_swaps("rose", "hello", big_limit)   # Substitute: r->h, o->e, s->l, e->l, length difference of 1.
  5
  """

  # BEGIN PROBLEM 6
  if len(start) == 0 or len(goal) == 0: # Base case (either of the words has length 0)
    return abs(len(start)-len(goal))
  elif limit < 0: # If we've exceeded the limit
    return 1 # To return 1 larger than the limit
  elif start[0] != goal[0]: # Check the first character
    return 1 + sphinx_swaps(start[1:],goal[1:],limit-1)
  else:
    return sphinx_swaps(start[1:],goal[1:],limit)
  # END PROBLEM 6

def minimum_mewtations(start, goal, limit):
  """A diff function that computes the edit distance from START to GOAL.
  This function takes in a string START, a string GOAL, and a number LIMIT.

  Arguments:
    start: a starting word
    goal: a goal word
    limit: a number representing an upper bound on the number of edits

  >>> big_limit = 10
  >>> minimum_mewtations("cats", "scat", big_limit)     # cats -> scats -> scat
  2
  >>> minimum_mewtations("purng", "purring", big_limit)   # purng -> purrng -> purring
  2
  >>> minimum_mewtations("ckiteus", "kittens", big_limit) # ckiteus -> kiteus -> kitteus -> kittens
  3
  """
  # BEGIN PROBLEM 7
  '''
  There are three different operations to be done here:
  - Adding a letter to start
  - Removing a letter from start
  - Changing a letter in start
  '''
  # Recursive function 
  def checkLetter(start, goal, count):
    # Returns a 0 if the two words are the same
    if start == goal:
      return 0
    # This function starts with a 0 for count, 
    # and it adds a one every time it does something
    # This if statement checks if you've gone over the limit,
    # and returns the limit if you've gone over.
    if count > limit:
      return limit
    # This checks if either word in the recursive function 
    # has run out of letters, returning the amount of remaining letters
    # in the remaining word.
    if len(start) == 0 or len(goal) == 0:
      return abs(len(start) - len(goal))
    # This checks if the start letters are the same, returning
    # the the next letters of both start and goal without increasing count
    if start[0] == goal[0]:
      return checkLetter(start[1:], goal[1:], count)
    # This is where most of the work gets done
    else:
      # These three are the three actions possible to take in modifying start and goal
      # add returns goal[1:] because it adds the letter to start and removes it while
      # also removing it from goal
      add = checkLetter(start, goal[1:], count + 1)
      # remove returns start[1:] because the it's only removing a letter from start, not goal
      remove = checkLetter(start[1:], goal, count + 1)
      # substitute returns start[1:] and goal[1:] because the letter in start is changed and then removed
      substitute = checkLetter(start[1:], goal[1:], count + 1)
      # This sort of creates a "tree," where every function calls another three recursive function,
      # exploring all the possibilities and returning the path through the tree that has the least value.
      return min(add, remove, substitute) + 1
  # plugs in the start, goal, and 0 for count and returns the result from checkLetter
  return checkLetter(start, goal, 0)
  # END PROBLEM 7

# STOP! #
# YOU DO NOT NEED TO EDIT ANY CODE BEYOND THIS POINT! #


def final_diff(start, goal, limit):
  """A diff function that takes in a string START, a string GOAL, and a number LIMIT.
  If you implement this function, it will be used."""
  assert False, 'Remove this line to use your final_diff function.'


FINAL_DIFF_LIMIT = 6  # REPLACE THIS WITH YOUR LIMIT

###########
# Phase 3 #
###########


def report_progress(sofar, prompt, user_id, upload):
  """Upload a report of your id and progress so far to the multiplayer server.
  Returns the progress so far.

  Arguments:
    sofar: a list of the words input so far
    prompt: a list of the words in the typing prompt
    user_id: a number representing the id of the current user
    upload: a function used to upload progress to the multiplayer server

  >>> print_progress = lambda d: print('ID:', d['id'], 'Progress:', d['progress'])
  >>> # The above function displays progress in the format ID: __, Progress: __
  >>> print_progress({'id': 1, 'progress': 0.6})
  ID: 1 Progress: 0.6
  >>> sofar = ['how', 'are', 'you']
  >>> prompt = ['how', 'are', 'you', 'doing', 'today']
  >>> report_progress(sofar, prompt, 2, print_progress)
  ID: 2 Progress: 0.6
  0.6
  >>> report_progress(['how', 'aree'], prompt, 3, print_progress)
  ID: 3 Progress: 0.2
  0.2
  """
  # BEGIN PROBLEM 8
  "*** YOUR CODE HERE ***"
  # END PROBLEM 8


def time_per_word(words, times_per_player):
  """Given timing data, return a match dictionary, which contains a
  list of words and the amount of time each player took to type each word.

  Arguments:
    words: a list of words, in the order they are typed.
    times_per_player: A list of lists of timestamps including the time
              the player started typing, followed by the time
              the player finished typing each word.

  >>> p = [[75, 81, 84, 90, 92], [19, 29, 35, 36, 38]]
  >>> match = time_per_word(['collar', 'plush', 'blush', 'repute'], p)
  >>> match["words"]
  ['collar', 'plush', 'blush', 'repute']
  >>> match["times"]
  [[6, 3, 6, 2], [10, 6, 1, 2]]
  """
  # BEGIN PROBLEM 9
  "*** YOUR CODE HERE ***"
  # END PROBLEM 9


def fastest_words(match):
  """Return a list of lists of which words each player typed fastest.

  Arguments:
    match: a match dictionary as returned by time_per_word.

  >>> p0 = [5, 1, 3]
  >>> p1 = [4, 1, 6]
  >>> fastest_words(match(['Just', 'have', 'fun'], [p0, p1]))
  [['have', 'fun'], ['Just']]
  >>> p0  # input lists should not be mutated
  [5, 1, 3]
  >>> p1
  [4, 1, 6]
  """
  player_indices = range(len(
    match["times"]))  # contains an *index* for each player
  word_indices = range(len(
    match["words"]))  # contains an *index* for each word
  # BEGIN PROBLEM 10
  "*** YOUR CODE HERE ***"
  # END PROBLEM 10


def match(words, times):
  """A dictionary containing all words typed and their times.

  Arguments:
    words: A list of strings, each string representing a word typed.
    times: A list of lists for how long it took for each player to type
      each word.
      times[i][j] = time it took for player i to type words[j].

  Example input:
    words: ['Hello', 'world']
    times: [[5, 1], [4, 2]]
  """
  assert all([type(w) == str
        for w in words]), 'words should be a list of strings'
  assert all([type(t) == list
        for t in times]), 'times should be a list of lists'
  assert all([isinstance(i, (int, float)) for t in times
        for i in t]), 'times lists should contain numbers'
  assert all([len(t) == len(words)
        for t in times]), 'There should be one word per time.'
  return {"words": words, "times": times}


def word_at(match, word_index):
  """A utility function that gets the word with index word_index"""
  assert 0 <= word_index < len(
    match["words"]), "word_index out of range of words"
  return match["words"][word_index]


def time(match, player_num, word_index):
  """A utility function for the time it took player_num to type the word at word_index"""
  assert word_index < len(match["words"]), "word_index out of range of words"
  assert player_num < len(
    match["times"]), "player_num out of range of players"
  return match["times"][player_num][word_index]


def match_string(match):
  """A helper function that takes in a match dictionary and returns a string representation of it"""
  return f"match({match['words']}, {match['times']})"


enable_multiplayer = False  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
  """Measure typing speed and accuracy on the command line."""
  paragraphs = lines_from_file('data/sample_paragraphs.txt')
  select = lambda p: True
  if topics:
    select = about(topics)
  i = 0
  while True:
    reference = choose(paragraphs, select, i)
    if not reference:
      print('No more paragraphs about', topics, 'are available.')
      return
    print('Type the following paragraph and then press enter/return.')
    print(
      'If you only type part of it, you will be scored only on that part.\n'
    )
    print(reference)
    print()

    start = datetime.now()
    typed = input()
    if not typed:
      print('Goodbye.')
      return
    print()

    elapsed = (datetime.now() - start).total_seconds()
    print("Nice work!")
    print('Words per minute:', wpm(typed, elapsed))
    print('Accuracy:    ', accuracy(typed, reference))

    print('\nPress enter/return for the next paragraph or type q to quit.')
    if input().strip() == 'q':
      return
    i += 1


@main
def run(*args):
  """Read in the command-line argument and calls corresponding functions."""
  import argparse
  parser = argparse.ArgumentParser(description="Typing Test")
  parser.add_argument('topic', help="Topic word", nargs='*')
  parser.add_argument('-t', help="Run typing test", action='store_true')

  args = parser.parse_args()
  if args.t:
    run_typing_test(args.topic)
