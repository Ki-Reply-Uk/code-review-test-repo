#
# Copyright (c) 2010, Andrew M. Kuchling
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import random, string

letter_stats={'a': (0, 2, 2, 1, 0), 'b':(2, 0, 0, 3, 1),
                  'c': (1, 2, 0, 0, 0), 'd':(1, 0, 0, 0, 1),
                  'e': (0, 3, 0, 3, 1), 'f':(0, 3, 0, 2, 1),
                  'g': (1, 2, 0, 1, 1), 'h':(0, 4, 0, 1, 2),
                  'i': (0, 2, 0, 0, 1), 'j':(1, 2, 0, 0, 1),
                  'k': (0, 4, 2, 0, 1), 'l':(0, 2, 0, 1, 1),
                  'm': (0, 2, 2, 0, 2), 'n':(0, 2, 1, 0, 2),
                  'o': (1, 0, 0, 0, 0), 'p':(1, 1, 0, 2, 1),
                  'q': (1, 2, 1, 0, 0), 'r':(1, 2, 1, 0, 1),
                  's': (1, 2, 0, 0, 0), 't':(0, 3, 0, 1, 1),
                  'u': (1, 2, 0, 0, 2), 'v':(0, 2, 2, 0, 0),
                  'w': (0, 2, 4, 0, 0), 'x':(0, 4, 2, 0, 0),
                  'y': (0, 3, 2, 0, 1), 'z':(0, 2, 1, 2, 0)}

CURVES=0 ; LOOSE_ENDS=1 ; OBLIQUES=2 ; HORIZONTALS=3 ; VERTICALS=4

questions={'curves':CURVES, 'looseends':LOOSE_ENDS,
           'obliques':OBLIQUES, 'diagonals':OBLIQUES,
           'horizontals':HORIZONTALS, 'verticals':VERTICALS}

def play_once():
    choice = random.choice(string.ascii_lowercase)
    possibilities = string.ascii_lowercase
    asked = []

    while True:
        query = get_user_input()
        if len(query) == 1:
            handle_guess(query, possibilities)
        elif query in questions:
            handle_question(query, choice, possibilities, asked)
        else:
            print("I don't understand the question.")

print("""This is a guessing game about capital letters.
You can ask various questions about the features of the letter:
curves, loose ends, obliques (or diagonals), horizontals, verticals.
To make a guess, just enter the letter of your choice.

Sample transcript:
        Next? curves?
        1.
        Good question.
        Next? c
        You don't have enough information yet.
        How do you know it isn't s, for example?
        Next? horizontals?
        0.
        Next? s
        You don't have enough information yet.
        How do you know it isn't c, for example?
""")

play_once()
raw_input("Press Return>")

def get_user_input():
    while True:
        try:
            query = raw_input('Next? ').strip().lower()
            return ''.join(filter(str.isalpha, query))
        except (EOFError, KeyboardInterrupt):
            print('\nOK; give up if you like.')
            return ""

def handle_guess(query, possibilities):
    if query not in possibilities:
        print("Wrong! That guess is inconsistent with the information you've been given.")
    elif len(possibilities) > 1:
        print("You don't have enough information yet.")
        temp = [x for x in possibilities if x != query]
        r = random.choice(temp)
        print(f"How do you know it isn't {r}, for example?")
    else:
        print("Yes, you've done it. Good work!")

def handle_question(query, choice, possibilities, asked):
    field = questions[query]
    result = letter_stats[choice][field]
    original_length = len(possibilities)
    possibilities = [letter for letter in possibilities if letter_stats[letter][field] == result]
    new_length = len(possibilities)
    if field in asked:
        print("You asked me that already.")
        print(f"The answer is the same as before: {result}.")
    else:
        asked.append(field)
        print(f"{result}.")
    if original_length == new_length:
        print('That was a wasted question; it did not exclude any possibilities.')
    elif new_length < original_length / 2 or new_length == 1:
        print("Good question.")
