from random import randrange

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from BattleBot import BattleBot


class LittleTimmyBot(BattleBot):

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
                    self.choose_switch(party, randrange(len(party)))  # TODO Choose best type-effectiveness
                    continue
                self.battle_logger.log_turn(self.Driver)
                self.read_team(BattleBot.OPPONENT_SIDE)
                self.choose_action()
                self.battle_logger.turn += 1
            except (NoSuchElementException, TimeoutException):
                continue

    def choose_action(self):
        if self.active_fainted():
            party = self.party_options()
            self.choose_switch(party, randrange(len(party)))  # TODO Choose best type-effectiveness
        else:
            # TODO Get Player and Opponent Type
            options, has_z, mega_elem = self.move_options(modded=True)
            strongest, pick = 0.0, ''
            for v, m in options:
                calc = self.damage_calc('', m.type, '', m.base_power)
                if calc > strongest:
                    strongest = calc
                    pick = v
            if pick == '':
                self.choose_move(options[randrange(len(options))][0], has_z, mega_elem)
            else:
                self.choose_move(pick, has_z, mega_elem)
