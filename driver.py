import random
import string

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebDriver:
    driver = webdriver.Edge()

    def __init__(self):
        self.driver.get('https://play.pokemonshowdown.com')

    def wait_for_element(self, val, by=By.ID, time=30):
        try:
            WebDriverWait(self.driver, time).until(
                EC.presence_of_element_located((by, val))
            )
        except NoSuchElementException:
            print("ERROR: Timed out waiting for webpage")

    def wait_and_click(self, val, by=By.ID):
        self.wait_for_element(val, by=by)
        self.driver.find_element(value=val, by=by).click()

    def setup_account(self):
        # Mute audio
        self.wait_and_click("openSounds", by=By.NAME)
        self.wait_and_click("muted", by=By.NAME)
        # Login
        self.wait_for_element("login", by=By.NAME)
        self.driver.maximize_window()
        self.driver.find_element(value="login", by=By.NAME).click()
        self.wait_for_element("username", by=By.NAME)
        # Random bot name
        botName = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(18))
        self.driver.find_element(value="username", by=By.NAME).send_keys(botName)
        self.driver.find_element(value="username", by=By.NAME).submit()
        self.wait_for_element("username", by=By.CLASS_NAME)

    def initiate_battle(self):
        # Select Gen 7
        self.wait_and_click("format", by=By.NAME)
        self.wait_for_element("selectFormat", by=By.NAME)
        self.driver.find_element(value="//button[text()='[Gen 7] Random Battle']", by=By.XPATH).click()
        # Find battle
        self.wait_and_click("search", by=By.NAME)
        # Wait for battle to start
        self.wait_for_element("movemenu", by=By.CLASS_NAME)

    def run(self):
        self.setup_account()
        self.initiate_battle()
        # Run battle bot


if __name__ == '__main__':
    WebDriver().run()
