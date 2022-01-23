from pathlib import Path
import re

guess1 = ['_', 'i', 'r', '_', 't']

def solve_wordle(possible_answers, guess_results):


    results = []

    for answer in possible_answers:
        if len(answer) != len(guess_results):
            possible_answers.remove(answer)
        

    for answer in possible_answers:    
        valid = True    
        for n in range(len(guess1)):
            if guess_results[n] == '_':
                pass
            else:
                if answer[n] != guess_results[n]:
                    valid = False
                    break
        if valid:
                results.append(answer)
                        


    print(results)


capitals = re.compile('[A-Z]')

with open("/home/bill/Code/python_code/wordle_solver/word_list.txt") as word_list:
    words = [word.strip() for word in word_list.readlines() if len(word.strip()) == 5 and not capitals.match(word[0])]
    solve_wordle(possible_answers=words, guess_results=guess1)