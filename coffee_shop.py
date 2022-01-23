from enum import Enum
from pathlib import Path
import re

guess1 = ['_', 'i', 'r', '_', 't']

class DataState(Enum):
    white = "empty"
    grey = "absent"
    yellow = "present"
    green = "correct"


def solve_wordle(answer_dict, guess, results):


    results = []

    for answer in answer_dict:
        if len(answer) != len(guess):
            answer_dict.remove(answer)
        

    for answer in answer_dict:    
        valid = True    
        for n in range(len(guess1)):
            if guess[n] == '_':
                pass
            else:
                if answer[n] != guess[n]:
                    valid = False
                    break
        if valid:
                results.append(answer)
                        


    print(results)


capitals = re.compile('[A-Z]')

with open("/home/bill/Code/python_code/wordle_solver/word_list.txt") as word_list:
    words = [word.strip() for word in word_list.readlines() if len(word.strip()) == 5 and not capitals.match(word[0])]
    solve_wordle(answer_dict=words, guess=guess1, results=None)