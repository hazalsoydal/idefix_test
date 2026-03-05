from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import time


class IdefixHomePage(BasePage):
    URL = "https://www.idefix.com"

    # Search box
    SEARCH_BOX = (By.CSS_SELECTOR, "input[type='search']")
    SEARCH_BOX_FALLBACK = (By.XPATH, "//input[@placeholder and (contains(@placeholder,'Ara') or contains(@placeholder,'ara') or contains(@placeholder,'search'))]")

    # App download modal close button
    APP_MODAL_CLOSE = (By.XPATH, "//div[contains(@class,'modal') or contains(@class,'Modal') or contains(@class,'popup') or contains(@class,'Popup')]//button[contains(@class,'close') or contains(@class,'Close') or contains(@aria-label,'kapat') or contains(@aria-label,'Kapat') or contains(@aria-label,'Close')]")
    APP_MODAL_X = (By.XPATH, "//button[normalize-space(text())='×' or normalize-space(text())='✕' or normalize-space(text())='✖']")
    APP_MODAL_SVG_CLOSE = (By.XPATH, "(//*[@role='dialog' or contains(@class,'modal') or contains(@class,'Modal') or contains(@class,'overlay') or contains(@class,'Overlay')]//button)[1]")

    # Notification popup
    NOTIF_DENY = (By.XPATH, "//button[contains(normalize-space(),'Hayır') or contains(normalize-space(),'HAYIR') or contains(normalize-space(),'hayır')]")

    # Cookie / GDPR banner
    COOKIE_ACCEPT = (By.XPATH, "//button[contains(normalize-space(),'Kabul') or contains(normalize-space(),'Onayla') or contains(normalize-space(),'Accept')]")

    def open(self):
        self.driver.get(self.URL)
        time.sleep(2)  # Give popups time to appear
        self.close_popups()

    def _click_if_present(self, locator, timeout=4):
        try:
            el = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            self.driver.execute_script("arguments[0].click();", el)
            time.sleep(0.5)
            return True
        except (TimeoutException, ElementClickInterceptedException):
            return False

    def _dismiss_overlay_by_js(self):
        """Force-hide common overlay/modal elements via JS."""
        self.driver.execute_script("""
            var selectors = [
                '[class*="modal"]', '[class*="Modal"]',
                '[class*="popup"]', '[class*="Popup"]',
                '[class*="overlay"]', '[class*="Overlay"]',
                '[role="dialog"]'
            ];
            selectors.forEach(function(sel) {
                document.querySelectorAll(sel).forEach(function(el) {
                    el.style.display = 'none';
                });
            });
            document.body.style.overflow = 'auto';
            document.body.style.position = '';
        """)
        time.sleep(0.3)

    def close_popups(self):
        """Try multiple strategies to close all popups."""
        # Strategy 1: click known close buttons
        self._click_if_present(self.APP_MODAL_CLOSE, timeout=3)
        self._click_if_present(self.APP_MODAL_X, timeout=2)
        self._click_if_present(self.APP_MODAL_SVG_CLOSE, timeout=2)

        # Strategy 2: deny notification prompt
        self._click_if_present(self.NOTIF_DENY, timeout=3)

        # Strategy 3: accept cookie banner
        self._click_if_present(self.COOKIE_ACCEPT, timeout=3)

        # Strategy 4: press Escape to close any open modal
        try:
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
            time.sleep(0.3)
        except Exception:
            pass

        # Strategy 5: JS force-hide all overlays as last resort
        self._dismiss_overlay_by_js()

    def _get_search_box(self, timeout=15):
        """Wait for and return the search box element."""
        for locator in [self.SEARCH_BOX, self.SEARCH_BOX_FALLBACK]:
            try:
                el = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located(locator)
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                time.sleep(0.3)
                return el
            except TimeoutException:
                continue
        raise TimeoutException("Search box not found with any selector")

    def wait_search_box(self, timeout=20):
        box = self._get_search_box(timeout)
        self.close_popups()
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(self.SEARCH_BOX)
        )

    def search(self, text):
        self.close_popups()

        box = self._get_search_box()

        # Use JS click+focus to bypass any overlay interception
        self.driver.execute_script("arguments[0].click(); arguments[0].focus();", box)
        time.sleep(0.3)

        # Clear and type
        box.clear()
        self.driver.execute_script("arguments[0].value = '';", box)
        box.send_keys(text)
        time.sleep(3)

        box.send_keys(Keys.RETURN)
