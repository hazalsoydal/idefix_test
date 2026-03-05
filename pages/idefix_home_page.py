from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


class IdefixHomePage(BasePage):
    URL = "https://www.idefix.com"

    # --- Locators (addresses of elements on the page) ---
    SEARCH_BOX  = (By.CSS_SELECTOR, "input[type='search']")
    NOTIF_DENY  = (By.XPATH, "//button[contains(normalize-space(),'Hayır')]")
    COOKIE_BTN  = (By.XPATH, "//button[contains(normalize-space(),'Kabul') or contains(normalize-space(),'Onayla')]")
    MODAL_CLOSE = (By.XPATH, "(//*[@role='dialog' or contains(@class,'modal') or contains(@class,'overlay')]//button)[1]")

    # --- Public methods ---

    def open(self):    #go to the website diyo yani
        self.driver.get(self.URL)
        time.sleep(2)        # wait for popups to appear
        self.close_popups()

    def close_popups(self):
        self._close_if_present(self.MODAL_CLOSE)   #try to click diyo ama if its not here dont crush it diyo
        self._close_if_present(self.NOTIF_DENY)    # "Hayır" notification button
        self._close_if_present(self.COOKIE_BTN)    # cookie banner
        # press Escape as a final safety net
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)

    def wait_search_box(self): #burda da wait until search box is ready to click diyo yani
        return WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.SEARCH_BOX)
        )

    def search(self, text):
        self.close_popups()
        box = self.wait_search_box()
        self.driver.execute_script("arguments[0].click(); arguments[0].focus();", box)
        box.clear()
        box.send_keys(text)
        time.sleep(3)        # wait so you can see what was typed
        box.send_keys(Keys.RETURN)

    # --- Private helper ---

    def _close_if_present(self, locator, timeout=3):
        """Click a button if it appears within timeout seconds. Skips if not found."""
        try:
            btn = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            self.driver.execute_script("arguments[0].click();", btn)
            time.sleep(0.5)
        except TimeoutException:
            pass  # popup didn't appear, that's fine