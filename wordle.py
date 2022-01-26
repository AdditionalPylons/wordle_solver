from enum import Enum, auto
from random import choice

from selenium import webdriver
from selenium.webdriver.remote.webelement import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep


class DataState(Enum):
    blank = "empty"
    white = "tbd"
    grey = "absent"
    yellow = "present"
    green = "correct"

class Strategy(Enum):
    brute_force = auto()
    rank_by_letter = auto()
    rank_by_word = auto()

ALL_WHITES = [DataState.white for _ in range(5)]


def open_site(driver):
    site = "https://www.powerlanguage.co.uk/wordle/"
    driver.get(site)
    sleep(1)

def close_overlay(driver):
    game_app_shadow = driver.find_element(By.CSS_SELECTOR, 'body>game-app').shadow_root
    game_modal_shadow = game_app_shadow.find_element(By.CSS_SELECTOR, 'game-modal').shadow_root

    close_button = game_modal_shadow.find_element(By.CSS_SELECTOR, 'game-icon')
    close_button.click()

def make_guess(driver, word):
    actions = ActionChains(driver)
    actions.send_keys(word + Keys.ENTER)
    actions.perform()
    sleep(2)

def clear_guess(driver):
    actions = ActionChains(driver)
    actions.send_keys([Keys.BACKSPACE for _ in range(5)])
    actions.perform()

def get_result(driver, row_num):
    row_num -= 1
    result = []

    for tile_num in range(5):
        game_app_shadow = driver.find_element(By.CSS_SELECTOR, 'body>game-app').shadow_root
        game_theme_manager= game_app_shadow.find_element(By.CSS_SELECTOR, 'game-theme-manager')
        game = game_theme_manager.find_element(By.CSS_SELECTOR, '#game')
        board_container = game.find_element(By.CSS_SELECTOR, '#board-container')
        board = board_container.find_element(By.CSS_SELECTOR, '#board')
        game_row_shadow = board.find_elements(By.CSS_SELECTOR, 'game-row')[row_num].shadow_root
        game_tile = game_row_shadow.find_elements(By.CSS_SELECTOR, 'game-tile')[tile_num]

        value = game_tile.get_attribute('evaluation')

        if value is None:
            result = ALL_WHITES
            break

        result.append(DataState(value))
        
    return result

def get_possible_answers(guess=None, result=None, answer_dict=None):
    if guess == answer_dict == result == None:
        with open("/home/bill/Code/python_code/wordle_solver/word_list.txt") as word_list:
            answer_dict = (word.strip() for word in word_list.readlines() if len(word.strip()) == 5 and word.strip().isalpha())
            return answer_dict

    possible_answers = []

        
    for answer in answer_dict:
        answer = answer.casefold()
        letter_set = set(answer)
        valid = True
        seen_letters = set()

        if result == ALL_WHITES:
            possible_answers = answer_dict
            valid = False
            break

        else:
            for index, letter in enumerate(guess):

                # Handle grey
                if result[index] == DataState.grey:
                    if letter in seen_letters:
                        valid = True
                        pass
                    elif letter in letter_set:
                        valid = False
                        break

                # Handle yellow
                elif result[index] == DataState.yellow:
                    if answer[index] == letter or letter not in letter_set:
                        valid = False
                        break

                # Handle green
                elif result[index] == DataState.green:
                    if answer[index] != letter:
                        valid = False
                        break
                
                seen_letters.add(letter)
                
        if valid:
                possible_answers.append(answer)

    if len(possible_answers) == 0:
        raise ValueError("There must be at least one answer left to try!") 

    return possible_answers

def get_next_guess(answer_dict: dict, is_first_guess: bool, seed: str, strategy: Strategy):
    if seed and is_first_guess:
        next_guess = seed

    elif strategy == Strategy.brute_force:
        next_guess = choice(answer_dict)

    elif strategy == Strategy.rank_by_letter:
        best_score = 0
        next_guess = None
        
        # 0-indexed for comparison
        letter_rankings = {
            0: ["s", "a", "r", "e", "o", "i"],
            1: ["a", "o", "e", "i", "r", "s"],
            2: ["r", "a", "i", "o", "e", "s"],
            3: ["e", "a", "i", "o", "r", "s"],
            4: ["s", "e", "a", "r", "o", "i"],
        }
        for answer in answer_dict:
            score = 0
            for index, letter in enumerate(answer):
                for ranked_index, ranked_letter in enumerate(letter_rankings[index]):
                    if letter == ranked_letter:
                        score += (6-(ranked_index)) # Reverse ranking order and credit end of list, i.e. index of 0 == score of 6
            if score > best_score:
                best_score = score
                next_guess = answer
    
        if not next_guess:
            next_guess = choice(answer_dict)

    return next_guess

def solve():
    with webdriver.Chrome() as driver:
        result = None
        row_num = 1
        answer_dict = None
        guess = None
        is_first_guess = True
        seed = "roate"

        open_site(driver)
        close_overlay(driver)
        while result != [DataState.green for _ in range(5)]:
            answer_dict = get_possible_answers(guess=guess, result=result, answer_dict=answer_dict)
            print(answer_dict)
            guess = get_next_guess(answer_dict, is_first_guess=is_first_guess, seed=seed, strategy=Strategy.rank_by_letter)
            is_first_guess = False
            print(guess)
            make_guess(driver, guess)
            result = get_result(driver, row_num)
            print(result)
            if result == ALL_WHITES:
                clear_guess(driver)
                guess = choice(answer_dict)
            else:
                row_num += 1

if __name__ == '__main__':
    solve()
