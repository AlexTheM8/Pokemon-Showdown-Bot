import random
import string

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebDriver:

    def __init__(self):
        self.driver = webdriver.Edge()
        self.driver.get('https://play.pokemonshowdown.com')

    def wait_for_element(self, val, by=By.NAME, time=30):
        try:
            WebDriverWait(self.driver, time).until(EC.presence_of_element_located((by, val)))
        except NoSuchElementException:
            print("ERROR: Timed out waiting for webpage")

    def wait_and_click(self, val, by=By.NAME):
        self.wait_for_element(val, by=by)
        self.driver.find_element(value=val, by=by).click()

    def setup_account(self):
        # Hide
        self.wait_for_element("closeHide")
        self.driver.maximize_window()
        self.wait_and_click("closeHide")
        # Mute audio
        self.wait_and_click("openSounds")
        self.wait_and_click("muted")
        # Login
        self.wait_and_click("login")
        self.wait_for_element("username")
        # Random bot name
        botName = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(18))
        self.driver.find_element(value="username", by=By.NAME).send_keys(botName)
        self.driver.find_element(value="username", by=By.NAME).submit()
        self.wait_for_element("username", by=By.CLASS_NAME)

    def set_format(self):
        # Select Gen 7
        self.wait_and_click("format")
        self.wait_for_element("selectFormat")
        # ac = ActionChains(self.driver)
        # format_elem = self.driver.find_element(value="//button[text()='[Gen 7] Random Battle']", by=By.XPATH)
        # ac.move_to_element(format_elem).perform()
        self.wait_and_click("//button[text()='[Gen 7] Random Battle']", by=By.XPATH)

    def next_battle(self):
        self.wait_and_click("closeAndMainMenu")

    def run(self):
        self.setup_account()
        self.set_format()
        self.wait_and_click("search")
