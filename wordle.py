from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from pathlib import Path
from urllib.request import urlretrieve
from typing import List
from time import sleep

with webdriver.Chrome(Path.cwd().joinpath("chromedriver")) as driver:
    site = "https://www.powerlanguage.co.uk/wordle/"
    driver.get(site)



    root = driver.find_element_by_xpath("/html/body/game-app")

    sleep(5)
    shadow_dom1 = driver.execute_script("return arguments[0].shadowRoot;", root)

    shadow_dom2 = shadow_dom1.find_element_by_xpath("/game-theme-manager")

