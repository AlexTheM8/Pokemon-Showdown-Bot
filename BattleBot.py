from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from BattleLogger import BattleLogger
from driver import WebDriver


class BattleBot:
    SELF_SIDE, OPPONENT_SIDE = 1, 2

    def __init__(self):
        self.battle_logger = BattleLogger()
        self.Driver = WebDriver()
        self.Driver.run()
        self.in_battle = True
        self.turn = 0

    def read_team(self, side):
        # Read available Pokemon & Moves of self & opponent
        ac = ActionChains(self.Driver.driver)
        if side == self.SELF_SIDE and self.turn == 0:
            # Read active Pokemon Ability
            # TODO Issue here
            self.Driver.wait_for_element("div[data-id='p1a']", by=By.CSS_SELECTOR)
            ac.move_to_element(self.Driver.driver.find_element(value="//div[@class='has-tooltip'][@data-id='p1a']",
                                                               by=By.XPATH)).perform()
            self.Driver.wait_for_element("div[class='tooltip tooltip-activepokemon']", by=By.CSS_SELECTOR)
            temp_elm = self.Driver.driver.find_element(value="//*[contains(text(), 'Ability:')]", by=By.XPATH)
            ability = temp_elm.find_element(value='./..', by=By.XPATH).text.replace('Ability: ', '')
            active_poke_name = self.Driver.driver.find_element(
                value="//div[contains(@class, 'statbar rstatbar')]/strong", by=By.XPATH).text.strip().split(' ')[0]
            # Read active Pokemon moves
            active_poke_moves = []
            for i in range(1, 5):
                move = self.Driver.driver.find_element(value="//button[@name='chooseMove'][@value='{}']"
                                                       .format(i), by=By.XPATH).get_attribute('data-move')
                active_poke_moves.append(move)
            self.battle_logger.update_data(BattleLogger.MOVE_INFO, active_poke_name, active_poke_moves)
            self.battle_logger.update_data(BattleLogger.ABILITY_INFO, active_poke_name, [ability])
            # Read team Pokemon & Moves
            for i in range(1, 6):
                # Get Pokemon name
                poke_elem = self.Driver.driver.find_element(value="//button[@name='chooseSwitch'][@value='{}']"
                                                            .format(i), by=By.XPATH)
                team_pokemon = poke_elem.text
                ac.move_to_element(poke_elem).perform()
                self.Driver.wait_for_element("div[class='tooltip tooltip-switchpokemon']", by=By.CSS_SELECTOR)
                # Get Pokemon moves
                team_moves = self.Driver.driver.find_element(value="section", by=By.CLASS_NAME).text.replace('• ', '').split('\n')
                # Get Pokemon ability
                temp_elm = self.Driver.driver.find_element(value="//*[contains(text(), 'Ability:')]", by=By.XPATH)
                ability = temp_elm.find_element(value='./..', by=By.XPATH).text.replace('Ability: ', '').split('/')[0].strip()
                self.battle_logger.update_data(BattleLogger.ABILITY_INFO, team_pokemon, [ability])
                self.battle_logger.update_data(BattleLogger.MOVE_INFO, team_pokemon, team_moves)
        else:
            pokemon_name = self.Driver.driver.find_element(
                value="//div[contains(@class, 'statbar lstatbar')]/strong", by=By.XPATH).text.strip().split(' ')[0]



