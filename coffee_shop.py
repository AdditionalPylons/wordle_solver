from enum import Enum
from pathlib import Path
import re


class DataState(Enum):
    white = "empty"
    grey = "absent"
    yellow = "present"
    green = "correct"

solution = 'crimp'

guess1 = 'audio'
result1 = [DataState.grey, DataState.grey, DataState.grey, DataState.yellow, DataState.grey]

guess2 = 'terms'
result2 = [DataState.grey, DataState.grey, DataState.yellow, DataState.green, DataState.grey]

guess3 = 'grimy'
result3 = [DataState.grey, DataState.green, DataState.green, DataState.green, DataState.grey]

def solve_wordle(answer_dict, guess, result):


    possible_answers = []

        
    for answer in answer_dict:
        answer = answer.casefold()
        answer_set = set(answer)
        valid = True
        for index, letter in enumerate(guess):

            if result[index] == DataState.grey:
                if letter in answer_set:
                    valid = False
                    break

            elif result[index] == DataState.yellow:
                if answer[index] == letter or letter not in answer_set:
                    valid = False
                    break

            elif result[index] == DataState.green:
                if answer[index] != letter:
                    valid = False
                    break
        if valid:
                possible_answers.append(answer)
                        


    return possible_answers


capitals = re.compile('[A-Z]')

with open("/home/bill/Code/python_code/wordle_solver/word_list.txt") as word_list:
    words = [word.strip() for word in word_list.readlines() if len(word.strip()) == 5]
    round_1 = solve_wordle(answer_dict=words, guess=guess1, result=result1)
    round_2 = (solve_wordle(answer_dict=round_1, guess=guess2, result=result2))
    print(solve_wordle(answer_dict=round_2, guess=guess3, result=result3))