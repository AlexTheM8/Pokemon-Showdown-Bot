from random import randrange

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from BattleBot import BattleBot


class RandomBot(BattleBot):

    def battle(self):
        # TODO End of battle
        self.read_team(BattleBot.SELF_SIDE)
        self.read_team(BattleBot.OPPONENT_SIDE)
        self.battle_timer()
        self.battle_logger.save_data()
        while self.in_battle():
            # Wait for next turn
            try:
                WebDriverWait(self.Driver.driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, self.ACTIVE_POKE_PATH))
                )
            except (TimeoutException, NoSuchElementException):
                continue
            # Log previous turn
            self.battle_logger.log_turn(self.Driver)
            # Read enemy team
            self.read_team(BattleBot.OPPONENT_SIDE)
            # Select action
            self.choose_action()
            self.battle_logger.turn += 1
            self.battle_logger.save_data()

    def choose_action(self):
        status = self.Driver.driver.find_element(value=self.ACTIVE_POKE_PATH, by=By.XPATH).get_attribute(
            'value').split(',')[1]
        if status == 'fainted':
            # Pokemon fainted
            n = randrange(len(self.slots))
            self.Driver.wait_and_click(self.CHOOSE_SWITCH_PATH.format(self.slots[n]), by=By.XPATH)
            del self.slots[n]
        else:
            # Check if there is a Z Move or Mega Evolution
            if self.Driver.driver.find_elements(value="//label[@class='megaevo']", by=By.XPATH):
                elem_type = self.Driver.driver.find_element(value="//label[@class='megaevo']", by=By.XPATH).text
                if 'Z-Power' in elem_type:
                    pass
                else:
                    pass
            # TODO Account for Z moves
            # TODO Always do Mega Evolution
            # TODO Account for U-Turn and Volt Switch
            # Choose one of 5 actions
            action = randrange(1, 6)
            if action < 5:
                selectable = []
                moves = self.Driver.driver.find_elements(value="//button[@name='chooseMove']", by=By.XPATH)
                for m in moves:
                    selectable.append(m.get_attribute('value'))
                # Select a move
                n = randrange(len(selectable))
                self.Driver.wait_and_click("//button[@name='chooseMove'][@value='{}']".format(selectable[n]),
                                           by=By.XPATH)
            else:
                # Switch pokemon
                n = randrange(len(self.slots))
                self.Driver.wait_and_click(self.CHOOSE_SWITCH_PATH.format(self.slots[n]), by=By.XPATH)
