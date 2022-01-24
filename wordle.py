from enum import Enum
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

def get_results(driver, row_num):
    row_num -= 1
    results = []

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
            results = ALL_WHITES
            break

        results.append(DataState(value))
        
    return results

def get_possible_answers(guess, result, answer_dict=None):
    if answer_dict == None:
        with open("/home/bill/Code/python_code/wordle_solver/word_list.txt") as word_list:
            answer_dict = (word.strip() for word in word_list.readlines() if len(word.strip()) == 5 and word.strip().isalpha())

    possible_answers = []

        
    for answer in answer_dict:
        answer = answer.casefold()
        letter_set = set(answer)
        valid = True

        if result == ALL_WHITES:
            possible_answers = answer_dict
            valid = False
            break

        else:
            for index, letter in enumerate(guess):

                # Handle grey
                if result[index] == DataState.grey:
                    if letter in letter_set:
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
                
        if valid:
                possible_answers.append(answer)

    if len(possible_answers) == 0:
        raise ValueError("There must be at least one answer left to try!") 

    return possible_answers

def solve():
    with webdriver.Chrome() as driver:
        results = None
        row_num = 1
        answer_dict = None
        guess = 'audio'

        open_site(driver)
        close_overlay(driver)
        while results != [DataState.green for _ in range(5)]:
            print(answer_dict)
            make_guess(driver, guess)
            results = get_results(driver, row_num)
            answer_dict = get_possible_answers(guess, results, answer_dict)
            print(answer_dict)
            guess = choice(answer_dict)
            if results == ALL_WHITES:
                clear_guess(driver)
                guess = choice(answer_dict)
            else:
                row_num += 1

solve()
