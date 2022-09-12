from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from BattleLogger import BattleLogger
from driver import WebDriver


class BattleBot:
    SELF_SIDE, OPPONENT_SIDE = 1, 2
    ACTIVE_POKE_PATH = "//button[@name='chooseDisabled'][@data-tooltip='switchpokemon|0']"
    CHOOSE_SWITCH_PATH = "//button[@name='chooseSwitch'][@value='{}']"
    OPP_POKE_PATH = "//div[@class='has-tooltip'][@data-id='p2a']"

    def __init__(self):
        self.battle_logger = BattleLogger()
        self.Driver = WebDriver()
        self.Driver.run()
        self.slots = [1, 2, 3, 4, 5]

    def read_team(self, side):
        # Read available Pokemon & Moves of self & opponent
        ac = ActionChains(self.Driver.driver)
        # TODO Check for Z Moves
        # Note: mega evolve is <label class="megaevo"> under "movemenu"
        if side == self.SELF_SIDE and self.battle_logger.turn == 0:
            poke_elem = self.Driver.driver.find_element(value=self.ACTIVE_POKE_PATH, by=By.XPATH)
            active_poke_name = poke_elem.text.split(',')[0]
            ac.move_to_element(poke_elem).perform()
            self.Driver.wait_for_element("div[class='tooltip tooltip-switchpokemon']", by=By.CSS_SELECTOR)
            # Get Pokemon ability
            temp_elm = self.Driver.driver.find_element(value="//*[contains(text(), 'Ability:')]", by=By.XPATH)
            ability = temp_elm.find_element(value='./..',
                                            by=By.XPATH).text.replace('Ability: ', '').split('/')[0].strip()
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
                poke_elem = self.Driver.driver.find_element(value=self.CHOOSE_SWITCH_PATH.format(i), by=By.XPATH)
                team_pokemon = poke_elem.text
                ac.move_to_element(poke_elem).perform()
                self.Driver.wait_for_element("div[class='tooltip tooltip-switchpokemon']", by=By.CSS_SELECTOR)
                # Get Pokemon moves
                team_moves = self.Driver.driver.find_element(value="section",
                                                             by=By.CLASS_NAME).text.replace('• ', '').split('\n')
                # Get Pokemon ability
                temp_elm = self.Driver.driver.find_element(value="//*[contains(text(), 'Ability:')]", by=By.XPATH)
                ability = temp_elm.find_element(value='./..',
                                                by=By.XPATH).text.replace('Ability: ', '').split('/')[0].strip()
                self.battle_logger.update_data(BattleLogger.ABILITY_INFO, team_pokemon, [ability])
                self.battle_logger.update_data(BattleLogger.MOVE_INFO, team_pokemon, team_moves)
        else:
            pokemon_name = self.Driver.driver.find_element(
                value="//div[contains(@class, 'statbar lstatbar')]/strong", by=By.XPATH).text.strip().split(' ')[0]
            ac.move_to_element(self.Driver.driver.find_element(value=self.OPP_POKE_PATH, by=By.XPATH)).perform()
            self.Driver.wait_for_element("div[class='tooltip tooltip-activepokemon']", by=By.CSS_SELECTOR)
            # Get abilities
            temp_elm = self.Driver.driver.find_element(
                value="//small[contains(text(), 'bilit')][contains(text(), ':')]", by=By.XPATH)
            if 'Ability' in temp_elm.text:
                # Ability known
                abilities = [temp_elm.find_element(value='./..',
                                                   by=By.XPATH).text.replace('Ability: ', '').split('/')[0].strip()]
            else:
                # Possible abilities
                abilities = temp_elm.find_element(value='./..',
                                                  by=By.XPATH).text.split(':')[1].strip().split(', ')
            self.battle_logger.update_data(BattleLogger.ABILITY_INFO, pokemon_name, abilities)
            # Get Pokemon moves
            ac.move_to_element(self.Driver.driver.find_element(value=self.OPP_POKE_PATH, by=By.XPATH)).perform()
            self.Driver.wait_for_element("div[class='tooltip tooltip-activepokemon']", by=By.CSS_SELECTOR)
            if self.Driver.driver.find_elements(value="section", by=By.CLASS_NAME):
                opp_moves = self.Driver.driver.find_element(value="section",
                                                            by=By.CLASS_NAME).text.replace('• ', '').split('\n')
                trimmed_moves = []
                for m in opp_moves:
                    trimmed_moves.append(m.split(' (')[0])
                self.battle_logger.update_data(BattleLogger.MOVE_INFO, pokemon_name, trimmed_moves)

    def in_battle(self):
        end_battle = self.Driver.driver.find_elements(value="//button[@class='button'][@name='closeAndMainMenu']",
                                                      by=By.XPATH)
        return not end_battle

    def battle_timer(self):
        self.Driver.wait_for_element("openTimer")
        timer = self.Driver.driver.find_element(value="openTimer", by=By.NAME)
        if "Timer" in timer.text:
            self.Driver.wait_and_click("openTimer")
            self.Driver.wait_and_click("timerOn")




