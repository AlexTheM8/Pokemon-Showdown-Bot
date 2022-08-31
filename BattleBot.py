from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from BattleLogger import BattleLogger
from driver import WebDriver

SELF_SIDE = 1
OPPONENT_SIDE = 2


class BattleBot:
    def __init__(self, driver: WebDriver):
        self.battle_logger = BattleLogger()
        self.Driver = driver
        self.in_battle = True

    def read_team(self, side):
        # Read available Pokemon & Moves of self & opponent
        if side == SELF_SIDE:
            pokemon_name = self.Driver.driver.find_element(
                value="//div[contains(@class, 'statbar rstatbar')]/strong", by=By.XPATH).text.strip().split(' ')[0]
            # Read moves
            for i in range(1, 5):
                move = self.Driver.driver.find_element(value="//div[@class='movemenu']/button[@value='{}']"
                                                       .format(str(i)), by=By.XPATH).get_attribute('data-move')
        else:
            pokemon_name = self.Driver.driver.find_element(
                value="//div[contains(@class, 'statbar lstatbar')]/strong", by=By.XPATH).text.strip().split(' ')[0]



