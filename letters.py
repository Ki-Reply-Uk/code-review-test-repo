
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

# Logic game
# From a program by Judith Haris, John Swets, and Wallace Feurzeig
# Reference: The Secret Guide to Computers, by Russ Walter, 18th ed 1993.
# Written in Python by A.M. Kuchling (amk@amk.ca)

# For each letter, we need the various characteristics:
# (curves, loose ends, obliques, horizontals, verticals).
# There should really be a sample character set for the user to look
# at; otherwise, there are ambiguities.  For example, does B have
# horizontals?  Does D?  How about P and R?

# There's a bug lurking in this data!  Can you catch it?
# (See the bottom of the program for the answer.)

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

# We'll define constants for the various statistics; each constant is
# equal to the position of the statistic in the tuples in
#letter_stats.
CURVES=0 ; LOOSE_ENDS=1 ; OBLIQUES=2 ; HORIZONTALS=3 ; VERTICALS=4

# This dictionary is used to map questions to corresponding
# statistics.  Note that different keys can map to the same value;
# for example, 'obliques' and 'diagonals' both map to the OBLIQUES constant.
questions={'curves':CURVES, 'looseends':LOOSE_ENDS,
           'obliques':OBLIQUES, 'diagonals':OBLIQUES,
           'horizontals':HORIZONTALS, 'verticals':VERTICALS}

# Play a single game

def play_once():
    # Choose a random number between 0 and 26, inclusive.
    choice=26*random.random()
    # Convert the numeric choice to a letter: 0->a, 1->b, etc.
    choice=chr(ord('a')+choice)

    #choice=raw_input("What should I choose?")          # (for debugging)

    # We'll track how many possibilities the user still has available.
    # Start with all of the letters.
    possibilities=string.lower("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    # We'll also track which questions have been asked, and chide the
    # user when he repeats a question.
    asked=[]

    # Loop forever; the play_once() function will exit by hitting a
    # 'return' statement inside the loop.
    while True:
        query = get_user_input()
        if len(query) == 1:
            handle_guess(query, possibilities)
        elif query in questions:
            handle_question(query, choice, possibilities, asked)
        else:
            print "I don't understand the question."

# Print the instructions
print """This is a guessing game about capital letters.
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
"""

# Play a single game
play_once()
raw_input("Press Return>")

# The solution to the bug-hunt is below...











# It's not a bug that the Python interpreter can catch; instead, it's
# a specification bug:
#
# 'C' and 'S' both have the same stats: 1 curve, 2 loose ends,
# and no obliques, horizontals, or verticals.  If either C or S is
# chosen as the computer's letter, the user can never get the right
# answer, because he/she can't narrow down the possibilities to just
# one!  To fix this, you'd have to add another statistic, like
# number of intersections or number of closed loops.  However, the
# statistic would have to be *different* for 'C' and 'S', and neither
# of those two suggestions qualify.  Can you think of a property to
# distinguish between the two letters?
def get_user_input():
    try:
        query = raw_input('Next? ')
        query = string.lower(query)
        query = filter(lambda x: x in string.lowercase, query)
        query = string.strip(query)
        return query
    except (EOFError, KeyboardInterrupt):
        print '\nOK; give up if you like.'
        return None

def handle_guess(query, possibilities):
    if query not in possibilities:
        print ("Wrong!  That guess is inconsistent with the information you've been given.\n"
               "I think you made that guess just to see what I would say.")
    elif len(possibilities) > 1:
        print "You don't have enough information yet."
        temp = filter(lambda x, query=query: x != query, possibilities)
        r = int(random.random() * len(temp))
        print "How do you know it isn't", temp[r] + ',', "for example?"
    else:
        print "Yes, you've done it.  Good work!"

def handle_question(query, choice, possibilities, asked):
    field = questions[query]
    result = letter_stats[choice][field]
    original_length = len(possibilities)
    possibilities = filter(lambda letter, letter_stats=letter_stats, field=field, result=result:
                           letter_stats[letter][field] == result, possibilities)
    new_length = len(possibilities)
    if field in asked:
        print "You asked me that already."
        print "The answer is the same as before:",
    else:
        asked.append(field)
    print str(result) + '.'
    if original_length == new_length:
        print 'That was a wasted question; it did not exclude any possibilities.'
    elif new_length < original_length / 2 or new_length == 1:
        print "Good question."
