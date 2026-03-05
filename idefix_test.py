from selenium import webdriver
from selenium.webdriver.chrome.service import Service

driver = webdriver.Chrome() #burda chrome'un fresh instance'ını aciyo
driver.get("https://www.idefix.com/?srsltid=AfmBOoro8zHzMfRIlkuIt92WsDcRoKpte7koW2HyPB7u-dU8ULTvqO5b") #burdaki get methodu most basic command. browsera go to this address and wait until the page finishes loading diyo

url = "https://www.idefix.com/?srsltid=AfmBOorjLNJdwWbEIW9OSvXqOecGhnmW57SCTOD-pZeD8WWCK7Ak4gpZ"

try:
    driver.get(url) #website ı ac

    driver.maximize_window()

    print("Page Title is:", driver.title) #burda dogru sitede miyiz diye check ediyo

    import time
    time.sleep(5) #burda da sayfayı 5 sn aik tutuyo ki calisio mu gorebil.

finally:
    driver.quit()