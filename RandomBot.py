from random import randrange

from selenium.common import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from BattleBot import BattleBot


class RandomBot(BattleBot):

    def battle(self):
        super().battle()
        while self.in_battle():
            # Wait for next turn
            try:
                WebDriverWait(self.Driver.driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, self.ACTIVE_POKE_PATH))
                )
            except (TimeoutException, NoSuchElementException):
                continue
            try:
                # Check if used switching move
                if not self.Driver.driver.find_elements(value="//div[@class='movemenu']", by=By.XPATH):
                    party = self.party_options()
                    self.choose_switch(party, randrange(len(party)))
                    continue
                self.battle_logger.log_turn(self.Driver)
                self.read_team(BattleBot.OPPONENT_SIDE)
                self.choose_action()
                self.battle_logger.turn += 1
            except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
                print("ERROR")
                continue
        self.battle_logger.log_turn(self.Driver)
        self.battle_logger.save_data()

    def choose_action(self):
        if self.active_fainted():
            party = self.party_options()
            self.choose_switch(party, randrange(len(party)))
        else:
            # TODO Check if accounts for arena trap
            # Limit to moves only if cannot switch
            party = self.party_options()
            if randrange(1, 6) < 5 or len(party) < 1:
                options, has_z, mega_elem = self.move_options()
                self.choose_move(options[randrange(len(options))][0], has_z, mega_elem)
            else:
                self.choose_switch(party, randrange(len(party)))
