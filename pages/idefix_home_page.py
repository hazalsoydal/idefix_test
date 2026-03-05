from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class IdefixHomePage(BasePage):
    URL = "https://www.idefix.com"

    # Search box (keep flexible)
    SEARCH_BOX = (By.CSS_SELECTOR, "input[type='search'], input[placeholder*='Ara'], input[name*='search']")

    # Notification popup buttons
    NOTIF_DENY = (By.XPATH, "//button[normalize-space()='Hayır' or normalize-space()='HAYIR']")
    NOTIF_ALLOW = (By.XPATH, "//button[contains(normalize-space(),'İzin Ver') or contains(normalize-space(),'Izin Ver')]")

    # Cookie popup (common patterns; may or may not exist)
    COOKIE_ACCEPT = (By.XPATH, "//button[contains(.,'Kabul') or contains(.,'Accept') or contains(.,'Onay')]")

    APP_MODAL_CLOSE = (
    By.CSS_SELECTOR, "button[aria-label='Close'], button[aria-label='Kapat'], .modal-close, .close, button.close")
    APP_MODAL_CLOSE_FALLBACK = (By.XPATH,
                                "//button[.='×' or normalize-space()='×' or @aria-label='Close' or @aria-label='Kapat'] | //*[@role='dialog']//button//*[name()='svg' or name()='path']/ancestor::button")

    def open(self):
        self.driver.get(self.URL)
        self.close_popups()

    def _click_if_present(self, locator, timeout=3):
        try:
            el = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
            el.click()
            return True
        except TimeoutException:
            return False

    def close_popups(self):
        # Try to close "download app" modal (X)
        self._click_if_present(self.APP_MODAL_CLOSE, timeout=4)
        self._click_if_present(self.APP_MODAL_CLOSE_FALLBACK, timeout=4)

        # Deny notification prompt if it appears
        self._click_if_present(self.NOTIF_DENY, timeout=3)

        # Accept cookies if it appears
        self._click_if_present(self.COOKIE_ACCEPT, timeout=3)

    def wait_search_box(self, timeout=25):
        # wait until it exists in DOM
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.SEARCH_BOX)
        )
        # close popups again (they can appear after load)
        self.close_popups()
        # now wait until clickable
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(self.SEARCH_BOX)
        )

    def search(self, text):
        self.close_popups()
        box = self.wait_search_box()
        box.clear()
        box.send_keys(text)
        box.submit()