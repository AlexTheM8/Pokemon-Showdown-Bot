import random
import string

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options

from util import util


class WebDriver:
    SELF_SIDE, OPP_SIDE = 1, 2
    ACTIVE_POKE_PATH = "//button[@name='chooseDisabled'][@data-tooltip='switchpokemon|0']"
    ACTIVE_STAGE_PATH = "//div[@class='has-tooltip'][@data-id='p1a']"
    CHOOSE_SWITCH_PATH = "//button[@name='chooseSwitch'][@value='{}']"
    FAINTED_SWITCH_PATH = "//button[@name='chooseDisabled'][@data-tooltip='switchpokemon|{}']"
    OPP_POKE_PATH = "//div[@class='has-tooltip'][@data-id='p2a']"

    def __init__(self, headless):
        options = Options()
        options.headless = headless
        self.driver = webdriver.Edge(options=options)
        self.driver.get('https://play.pokemonshowdown.com')
        self.AC = ActionChains(self.driver)
        self.botName = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(18))

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
        self.driver.find_element(value="username", by=By.NAME).send_keys(self.botName)
        self.driver.find_element(value="username", by=By.NAME).submit()
        self.wait_for_element("username", by=By.CLASS_NAME)

    def set_format(self):
        # Select Gen 7
        self.wait_and_click("format")
        self.wait_for_element("selectFormat")
        self.wait_and_click("//button[text()='[Gen 7] Random Battle']", by=By.XPATH)

    def in_battle(self):
        end_battle = self.driver.find_elements(value="//button[@class='button'][@name='closeAndMainMenu']",
                                               by=By.XPATH)
        return not end_battle

    def next_battle(self):
        self.wait_and_click("closeAndMainMenu")

    def get_type(self, side, num=0, poke_elem=None):
        tooltip_div = "//div[contains(@class, 'tooltip tooltip-')]"
        img_ext = "/h2/img[@class='pixelated'][@height='14']"
        types = []
        if poke_elem is None:
            if side == self.SELF_SIDE:
                self.wait_for_element(self.ACTIVE_POKE_PATH, by=By.XPATH)
                if num == 0:
                    poke_elem = self.driver.find_element(value=self.ACTIVE_STAGE_PATH, by=By.XPATH)
                else:
                    poke_elem = self.driver.find_element(value=self.CHOOSE_SWITCH_PATH.format(num), by=By.XPATH)
            else:
                self.wait_for_element("//div[contains(@class, 'statbar lstatbar')]/strong", by=By.XPATH)
                poke_elem = self.driver.find_element(value=self.OPP_POKE_PATH, by=By.XPATH)
        self.AC.move_to_element(poke_elem).perform()
        self.wait_for_element(tooltip_div, by=By.XPATH)
        self.wait_for_element(tooltip_div + img_ext, by=By.XPATH)
        poke_types = self.driver.find_elements(value=tooltip_div + img_ext, by=By.XPATH)
        for t in poke_types:
            types.append(t.get_attribute('alt'))
        return types

    def get_field_settings(self, side):
        base_xpath = "//div[@class='innerbattle']/*[5]/*[{}]/img[contains(@src, 'fx/{}')]"
        base_xpath_2 = "//div[@class='innerbattle']/*[5]/*[{}]/div[@class='sidecondition-{}']"
        base_xpath_3 = "//div[@class='innerbattle']/*[5]/*[{}]/img[contains(@src, 'substitute')]" \
                       "[contains(@style, 'opacity: 1')]"
        caltrop, rock, poison, web = 'caltrop', 'rock', 'poisoncaltrop', 'web'
        reflect, screen, auroraveil = 'reflect', 'lightscreen', 'auroraveil'
        num = 3 if side == self.SELF_SIDE else 2
        field = {
            util.FIELD_SPIKES: len(self.driver.find_elements(value=base_xpath.format(num, caltrop), by=By.XPATH)),
            util.FIELD_POISON: len(self.driver.find_elements(value=base_xpath.format(num, poison), by=By.XPATH)),
            util.FIELD_WEB: len(self.driver.find_elements(value=base_xpath.format(num, web), by=By.XPATH)),
            util.FIELD_STONES: 1 if self.driver.find_elements(value=base_xpath.format(num, rock), by=By.XPATH) else 0,
            util.FIELD_REFLECT: len(self.driver.find_elements(value=base_xpath_2.format(num, reflect), by=By.XPATH)),
            util.FIELD_SCREEN: len(self.driver.find_elements(value=base_xpath_2.format(num, screen), by=By.XPATH)),
            util.FIELD_AURORA_VEIL: len(self.driver.find_elements(value=base_xpath_2.format(num, auroraveil),
                                                                  by=By.XPATH)),
            util.FIELD_SUBSTITUTE: 1 if self.driver.find_elements(value=base_xpath_3.format(num), by=By.XPATH) else 0
        }
        return field

    def wait_for_next_turn(self):
        while self.in_battle():
            try:
                skip = self.driver.find_elements(value="//button[@name='goToEnd']", by=By.XPATH)
                if skip:
                    skip[0].click()
                WebDriverWait(self.driver, 0.1).until(
                    EC.presence_of_element_located((By.XPATH, self.ACTIVE_POKE_PATH))
                )
            except (TimeoutException, NoSuchElementException):
                continue
            return False
        return True

    def run(self):
        self.setup_account()
        self.set_format()
        self.wait_and_click("search")
