import pytest
from selenium import webdriver
from pages.idefix_home_page import IdefixHomePage

@pytest.fixture
def home_page():
    driver = webdriver.Chrome()
    driver.maximize_window()
    page = IdefixHomePage(driver)
    yield page
    driver.quit()

#Opens Chrome
#Creates the homepage object
#Gives it to the test
#Closes Chrome after test finishes

#bu conftest sadece browser olusturuyo ve sayfa nesnesini veriyo.