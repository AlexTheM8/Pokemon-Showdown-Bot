from random import randrange

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from BattleBot import BattleBot


class RandomBot(BattleBot):

    # TODO Check for forfeit if exception caught
    def battle(self):
        self.read_team(BattleBot.SELF_SIDE)
        self.battle_timer()
        while self.in_battle():
            # TODO Skip to End
            # Wait for next turn
            try:
                WebDriverWait(self.Driver.driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, self.ACTIVE_POKE_PATH))
                )
            except (TimeoutException, NoSuchElementException):
                continue
            # Check if used switching move
            if not self.Driver.driver.find_elements(value="//div[@class='movemenu']", by=By.XPATH):
                # Switch pokemon
                party = []
                self.Driver.wait_for_element("//button[@name='chooseSwitch']", by=By.XPATH)
                pokes = self.Driver.driver.find_elements(value="//button[@name='chooseSwitch']", by=By.XPATH)
                for p in pokes:
                    party.append(p.get_attribute('value'))
                n = randrange(len(party))
                self.Driver.wait_and_click(self.CHOOSE_SWITCH_PATH.format(party[n]), by=By.XPATH)
                continue
            # Log previous turn
            self.battle_logger.log_turn(self.Driver)
            # Read enemy team
            self.read_team(BattleBot.OPPONENT_SIDE)
            # Select action
            self.choose_action()
            self.battle_logger.turn += 1
            self.battle_logger.save_data()
        self.battle_logger.log_turn(self.Driver)
        self.battle_logger.save_data()

    def choose_action(self):
        status = self.Driver.driver.find_element(value=self.ACTIVE_POKE_PATH, by=By.XPATH).get_attribute(
            'value').split(',')[1]
        if status == 'fainted':
            # Pokemon fainted
            party = []
            pokes = self.Driver.driver.find_elements(value="//button[@name='chooseSwitch']", by=By.XPATH)
            for p in pokes:
                party.append(p.get_attribute('value'))
            n = randrange(len(party))
            self.Driver.wait_and_click(self.CHOOSE_SWITCH_PATH.format(party[n]), by=By.XPATH)
        else:
            # TODO Check if accounts for arena trap
            # Limit to moves only if cannot switch
            party = []
            pokes = self.Driver.driver.find_elements(value="//button[@name='chooseSwitch']", by=By.XPATH)
            for p in pokes:
                party.append(p.get_attribute('value'))
            # Choose actions
            if randrange(1, 6) < 5 or len(party) < 1:
                selectable = []
                has_z = False
                # Check if there is a Z Move or Mega Evolution
                has_z_mega = self.Driver.driver.find_elements(value="//label[@class='megaevo']", by=By.XPATH)
                if has_z_mega:
                    elem = has_z_mega[0]
                    if 'Z-Power' in elem.text:
                        # Check number of Z-moves
                        z_moves = self.Driver.driver.find_elements(
                            value="//div[@class='movebuttons-z']/button[@name='chooseMove']", by=By.XPATH)
                        for m in z_moves:
                            selectable.append('z' + m.get_attribute('value'))
                        has_z = True
                    else:
                        # Do Mega Evo
                        elem.click()
                if has_z:
                    moves = self.Driver.driver.find_elements(
                        value="//div[@class='movebuttons-noz']/button[@name='chooseMove']", by=By.XPATH)
                else:
                    moves = self.Driver.driver.find_elements(value="//button[@name='chooseMove']", by=By.XPATH)
                for m in moves:
                    selectable.append(m.get_attribute('value'))
                # Select a move
                n = randrange(len(selectable))
                move = selectable[n]
                if has_z:
                    if 'z' in move:
                        # Use Z-move
                        has_z_mega[0].click()
                        move = move.replace('z', '')
                        self.Driver.wait_and_click(
                            "//div[@class='movebuttons-z']/button[@name='chooseMove'][@value='{}']".format(move),
                            by=By.XPATH)
                    else:
                        self.Driver.wait_and_click(
                            "//div[@class='movebuttons-noz']/button[@name='chooseMove'][@value='{}']".format(move),
                            by=By.XPATH)
                else:
                    self.Driver.wait_and_click("//button[@name='chooseMove'][@value='{}']".format(move), by=By.XPATH)
            else:
                # Switch pokemon
                n = randrange(len(party))
                self.Driver.wait_and_click(self.CHOOSE_SWITCH_PATH.format(party[n]), by=By.XPATH)
