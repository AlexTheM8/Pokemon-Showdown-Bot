import time
from re import sub, findall

from selenium.common import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

import util
from BattleLogger import BattleLogger, Move
from driver import WebDriver

from util import type_effectiveness


class BattleBot:
    SELF_SIDE, OPPONENT_SIDE = 1, 2
    ACTIVE_POKE_PATH = "//button[@name='chooseDisabled'][@data-tooltip='switchpokemon|0']"
    CHOOSE_SWITCH_PATH = "//button[@name='chooseSwitch'][@value='{}']"
    OPP_POKE_PATH = "//div[@class='has-tooltip'][@data-id='p2a']"

    def __init__(self):
        self.battle_logger = BattleLogger()
        self.Driver = WebDriver()
        self.Driver.run()

    def battle(self):
        try:
            self.read_team(BattleBot.SELF_SIDE)
            self.battle_timer()
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
            pass

    def read_team(self, side):
        # Read available Pokemon & Moves of self & opponent
        ac = ActionChains(self.Driver.driver)
        if side == self.SELF_SIDE:
            if self.battle_logger.turn == 0:
                self.Driver.wait_for_element(self.ACTIVE_POKE_PATH, by=By.XPATH)
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
                    if move == 'Return 102':
                        move = 'Return'
                    active_poke_moves.append(move)
                self.battle_logger.update_data(BattleLogger.MOVE_INFO, active_poke_name, active_poke_moves)
                if '(base: ' not in ability and 'TOX' not in ability:
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
                    for idx, m in enumerate(team_moves):
                        if m == 'Return 102':
                            team_moves[idx] = 'Return'
                    # Get Pokemon ability
                    temp_elm = self.Driver.driver.find_element(value="//*[contains(text(), 'Ability:')]", by=By.XPATH)
                    ability = temp_elm.find_element(value='./..',
                                                    by=By.XPATH).text.replace('Ability: ', '').split('/')[0].strip()
                    if '(base: ' not in ability and 'TOX' not in ability:
                        self.battle_logger.update_data(BattleLogger.ABILITY_INFO, team_pokemon, [ability])
                    self.battle_logger.update_data(BattleLogger.MOVE_INFO, team_pokemon, team_moves)
        else:
            self.Driver.wait_for_element("//div[contains(@class, 'statbar lstatbar')]/strong", by=By.XPATH)
            elem_txt = self.Driver.driver.find_element(value="//div[contains(@class, 'statbar lstatbar')]/strong",
                                                       by=By.XPATH).text
            pokemon_name = sub(r'(.*) L[0-9]+', r'\1', elem_txt.strip()).strip().replace('�', "'")
            ac.move_to_element(self.Driver.driver.find_element(value=self.OPP_POKE_PATH, by=By.XPATH)).perform()
            self.Driver.wait_for_element("div[class='tooltip tooltip-activepokemon']", by=By.CSS_SELECTOR)
            # Get abilities
            temp_elm = self.Driver.driver.find_element(
                value="//small[contains(text(), 'bilit')][contains(text(), ':')]", by=By.XPATH)
            if 'Ability' in temp_elm.text:
                # Ability known
                abilities = [temp_elm.find_element(value='./..',
                                                   by=By.XPATH).text.replace('Ability: ', '').split('/')[0].strip()]
                if '(base: ' in abilities[0] or 'TOX' in abilities:
                    abilities[0] = ''
            else:
                # Possible abilities
                abilities = temp_elm.find_element(value='./..',
                                                  by=By.XPATH).text.split(':')[1].strip().split(', ')
            if pokemon_name != '':
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
                if pokemon_name != '':
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

    def reset(self):
        # TODO Reset battle info
        self.Driver.next_battle()
        self.battle_logger.reset()
        self.Driver.wait_and_click("search")

    def move_options(self, modded=False):
        options = []
        has_z = False
        # Check if there is a Z Move or Mega Evolution
        has_z_mega = self.Driver.driver.find_elements(value="//label[@class='megaevo']", by=By.XPATH)
        if has_z_mega:
            elem = has_z_mega[0]
            if 'Z-Power' in elem.text:
                elem.click()
                # Check number of Z-moves
                z_moves = self.Driver.driver.find_elements(
                    value="//div[@class='movebuttons-z']/button[@name='chooseMove']", by=By.XPATH)
                for m in z_moves:
                    move_data = self.get_move_data(m) if not modded else self.get_modded_move_data(m)
                    options.append(('z' + m.get_attribute('value'), move_data))
                has_z = True
                elem.click()
            else:
                # Do Mega Evo
                elem.click()
        if has_z:
            moves = self.Driver.driver.find_elements(
                value="//div[@class='movebuttons-noz']/button[@name='chooseMove']", by=By.XPATH)
        else:
            moves = self.Driver.driver.find_elements(value="//button[@name='chooseMove']", by=By.XPATH)
        for m in moves:
            move_data = self.get_move_data(m) if not modded else self.get_modded_move_data(m)
            options.append((m.get_attribute('value'), move_data))
        return options, has_z, has_z_mega

    def choose_move(self, move, has_z, mega_elem):
        if has_z:
            if 'z' in move:
                # Use Z-move
                mega_elem[0].click()
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

    def get_move_data(self, m):
        move_name = m.get_attribute('data-move')
        if move_name == 'Return 102':
            move_name = 'Return'
        if move_name not in self.battle_logger.move_map.keys():
            tooltip_div = "//div[contains(@class, 'tooltip tooltip-')]"
            ac = ActionChains(self.Driver.driver)
            elem_type = sub(r'^type-(.*) has-tooltip$', r'\1', m.get_attribute('class'))
            ac.move_to_element(m).perform()
            self.Driver.wait_for_element(tooltip_div, by=By.XPATH)
            self.Driver.wait_for_element(tooltip_div + "/h2/img[@class='pixelated']", by=By.XPATH)
            move_type = self.Driver.driver.find_elements(value=tooltip_div + "/h2/img[@class='pixelated']",
                                                         by=By.XPATH)[1].get_attribute('alt')
            if move_type != util.STATUS:
                base_text = self.Driver.driver.find_element(
                    value=tooltip_div + "/p[contains(text(), 'Base power: ')]", by=By.XPATH).text
                additional_text = sub(r'^Base power: (?:\d+)(?:\.)?(?:\d+)?(.*)$', r'\1', base_text).strip()
                base_text = sub(r'^Base power: ((?:\d+)(?:\.)?(?:\d+)?).*$', r'\1', base_text)
                if not base_text.replace('.', '').isnumeric():
                    base = 0.0
                else:
                    base = float(base_text)
                if additional_text != '':
                    nums = findall(r'\(((?:\d+)(?:\.)?(?:\d+)?)× from .*\)', additional_text)
                    for n in nums:
                        base /= float(n)
            else:
                base = 0.0
            move = Move(move_name, elem_type, move_type, base)
            self.battle_logger.update_move_info(move)
            return move
        return self.battle_logger.move_map[move_name]

    def get_modded_move_data(self, m):
        move_name = m.get_attribute('data-move')
        if move_name == 'Return 102':
            move_name = 'Return'
        tooltip_div = "//div[contains(@class, 'tooltip tooltip-')]"
        ac = ActionChains(self.Driver.driver)
        elem_type = sub(r'^type-(.*) has-tooltip$', r'\1', m.get_attribute('class'))
        ac.move_to_element(m).perform()
        self.Driver.wait_for_element(tooltip_div, by=By.XPATH)
        self.Driver.wait_for_element(tooltip_div + "/h2/img[@class='pixelated']", by=By.XPATH)
        move_type = self.Driver.driver.find_elements(value=tooltip_div + "/h2/img[@class='pixelated']",
                                                     by=By.XPATH)[1].get_attribute('alt')
        if move_type != util.STATUS:
            base_text = self.Driver.driver.find_element(
                value=tooltip_div + "/p[contains(text(), 'Base power: ')]", by=By.XPATH).text
            base_text = sub(r'^Base power: ((?:\d+)(?:\.)?(?:\d+)?).*$', r'\1', base_text)
            if not base_text.replace('.', '').isnumeric():
                base = 0.0
            else:
                base = float(base_text)
        else:
            base = 0.0
        return Move(move_name, elem_type, move_type, base)

    def active_fainted(self):
        status = self.Driver.driver.find_element(value=self.ACTIVE_POKE_PATH, by=By.XPATH).get_attribute(
            'value').split(',')[1]
        return status == 'fainted'

    def party_options(self):
        party = []
        pokes = self.Driver.driver.find_elements(value="//button[@name='chooseSwitch']", by=By.XPATH)
        for p in pokes:
            party.append(p.get_attribute('value'))
        return party

    def choose_switch(self, party, n):
        self.Driver.wait_and_click(self.CHOOSE_SWITCH_PATH.format(party[n]), by=By.XPATH)

    @staticmethod
    def damage_calc(player_type, move_type, opponent_type, base_power):
        # TODO Special, Physical
        if base_power == 0.0:
            return 0.0
        if type_effectiveness(move_type, opponent_type) == 0.0:
            return 0.0
        dmg = base_power
        if player_type == move_type:
            dmg *= 1.5
        for t in opponent_type:
            dmg *= type_effectiveness(move_type, t)
        return dmg
