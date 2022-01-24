from enum import Enum
from random import choice

from selenium import webdriver
from selenium.webdriver.remote.webelement import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep


class DataState(Enum):
    white = "empty"
    grey = "absent"
    yellow = "present"
    green = "correct"


def open_site(driver):
    site = "https://www.powerlanguage.co.uk/wordle/"
    driver.get(site)

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

def get_results(driver, row_num):
    row_num -= 1
    guess = []
    results = []

    for tile_num in range(5):
        game_app_shadow = driver.find_element(By.CSS_SELECTOR, 'body>game-app').shadow_root
        game_theme_manager= game_app_shadow.find_element(By.CSS_SELECTOR, 'game-theme-manager')
        game = game_theme_manager.find_element(By.CSS_SELECTOR, '#game')
        board_container = game.find_element(By.CSS_SELECTOR, '#board-container')
        board = board_container.find_element(By.CSS_SELECTOR, '#board')
        game_row_shadow = board.find_elements(By.CSS_SELECTOR, 'game-row')[row_num].shadow_root
        game_tile = game_row_shadow.find_elements(By.CSS_SELECTOR, 'game-tile')[tile_num]
        
        guess.append(game_tile.get_attribute('letter'))
        results.append(game_tile.get_attribute('evaluation'))
        
    return ''.join(guess), results

def get_possible_answers(guess, result, answer_dict=None):
    if answer_dict == None:
        with open("/home/bill/Code/python_code/wordle_solver/word_list.txt") as word_list:
            answer_dict = (word.strip() for word in word_list.readlines() if len(word.strip()) == 5 and word.strip().isalpha())

    possible_answers = []

        
    for answer in answer_dict:
        answer = answer.casefold()
        answer_set = set(answer)
        valid = True
        for index, letter in enumerate(guess):

            # Handle grey
            if result[index] == DataState.grey:
                if letter in answer_set:
                    valid = False
                    break

            # Handle yellow
            elif result[index] == DataState.yellow:
                if answer[index] == letter or letter not in answer_set:
                    valid = False
                    break

            # Handle green
            elif result[index] == DataState.green:
                if answer[index] != letter:
                    valid = False
                    break
        if valid:
                possible_answers.append(answer)
                        

    return possible_answers

def solve():
    with webdriver.Chrome() as driver:
        results = None
        open_site(driver)
        close_overlay(driver)
        #while results != [DataState.green for x in range(5)]:
        make_guess(driver, 'audio')
        make_guess(driver, 'terms')
        make_guess(driver, 'lisps')
        make_guess(driver, 'stink')

        print(get_results(driver, 1))
        print(get_results(driver, 2))
        print(get_results(driver, 3))
        print(get_results(driver, 4))


solve()
