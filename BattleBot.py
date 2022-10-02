from re import sub, findall, match

from selenium.common import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import util
from BattleLogger import BattleLogger, Move, Pokemon
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
        self.AC = ActionChains(self.Driver.driver)

    def battle(self):
        try:
            self.read_team(BattleBot.SELF_SIDE)
            self.battle_timer()
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
            pass
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
                    self.choose_switch()
                    continue
                self.battle_logger.log_turn(self.Driver)
                self.read_team(BattleBot.OPPONENT_SIDE)
                self.choose_action()
                self.battle_logger.turn += 1
            except (NoSuchElementException, TimeoutException, StaleElementReferenceException, ValueError):
                continue
        self.battle_logger.log_turn(self.Driver)
        self.battle_logger.save_data()

    def read_team(self, side):
        # Read available Pokemon & Moves of self & opponent
        if side == self.SELF_SIDE:
            if self.battle_logger.turn == 0:
                self.Driver.wait_for_element(self.ACTIVE_POKE_PATH, by=By.XPATH)
                active_poke_name = self.Driver.driver.find_element(value=self.ACTIVE_POKE_PATH,
                                                                   by=By.XPATH).text.split(',')[0]
                # Get Pokemon ability
                ability, item = self.get_ability_item(self.SELF_SIDE)
                # Read active Pokemon moves
                move_options, _, _ = self.move_options()
                active_poke_moves = [m[1].name for m in move_options]
                if active_poke_name != 'Ditto':
                    self.battle_logger.update_data(BattleLogger.MOVE_INFO, active_poke_name, active_poke_moves)
                    if '(base: ' not in ability and 'TOX' not in ability:
                        self.battle_logger.update_data(BattleLogger.ABILITY_INFO, active_poke_name, [ability])
                self.battle_logger.self_team.append(Pokemon(active_poke_name, ability, item, move_options,
                                                            self.get_stats()))
                # Read team Pokemon & Moves
                for i in range(1, 6):
                    # Get Pokemon name
                    poke_elem = self.Driver.driver.find_element(value=self.CHOOSE_SWITCH_PATH.format(i), by=By.XPATH)
                    team_pokemon = poke_elem.text
                    self.AC.move_to_element(poke_elem).perform()
                    self.Driver.wait_for_element("div[class='tooltip tooltip-switchpokemon']", by=By.CSS_SELECTOR)
                    # Get Pokemon moves
                    team_move_names = self.Driver.driver.find_element(
                        value="section", by=By.CLASS_NAME).text.replace('• ', '').split('\n')
                    for idx, m in enumerate(team_move_names):
                        if m == 'Return 102':
                            team_move_names[idx] = 'Return'
                    # Get Pokemon ability
                    ability, item = self.get_ability_item(self.SELF_SIDE, num=i)
                    if team_pokemon != 'Ditto':
                        if '(base: ' not in ability and 'TOX' not in ability:
                            self.battle_logger.update_data(BattleLogger.ABILITY_INFO, team_pokemon, [ability])
                        self.battle_logger.update_data(BattleLogger.MOVE_INFO, team_pokemon, team_move_names)
                    self.battle_logger.self_team.append(Pokemon(team_pokemon, ability, item))
        else:
            self.Driver.wait_for_element("//div[contains(@class, 'statbar lstatbar')]/strong", by=By.XPATH)
            elem_txt = self.Driver.driver.find_element(value="//div[contains(@class, 'statbar lstatbar')]/strong",
                                                       by=By.XPATH).text
            pokemon_name = sub(r'(.*) L[0-9]+', r'\1', elem_txt.strip()).strip().replace('�', "'")
            abilities, item = self.get_ability_item(self.OPPONENT_SIDE)
            if '(base: ' in abilities[0] or 'TOX' in abilities:
                abilities[0] = ''
            if pokemon_name != '' and pokemon_name != 'Ditto':
                self.battle_logger.update_data(BattleLogger.ABILITY_INFO, pokemon_name, abilities)
            # Get Pokemon moves
            self.AC.move_to_element(self.Driver.driver.find_element(value=self.OPP_POKE_PATH, by=By.XPATH)).perform()
            self.Driver.wait_for_element("div[class='tooltip tooltip-activepokemon']", by=By.CSS_SELECTOR)
            if self.Driver.driver.find_elements(value="section", by=By.CLASS_NAME):
                opp_moves = self.Driver.driver.find_element(value="section",
                                                            by=By.CLASS_NAME).text.replace('• ', '').split('\n')
                trimmed_moves = []
                for m in opp_moves:
                    trimmed_moves.append(m.split(' (')[0])
                if pokemon_name != '' and pokemon_name != 'Ditto':
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
        retry_count = 3
        success = False
        while not success:
            try:
                self.Driver.next_battle()
                self.battle_logger.reset()
                self.Driver.wait_and_click("search")
            except StaleElementReferenceException:
                if retry_count <= 0:
                    print('Retries exceeded')
                    exit(0)
                retry_count -= 1
            success = True

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
            elem_type = sub(r'^type-(.*) has-tooltip$', r'\1', m.get_attribute('class'))
            self.AC.move_to_element(m).perform()
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
        elem_type = sub(r'^type-(.*) has-tooltip$', r'\1', m.get_attribute('class'))
        self.AC.move_to_element(m).perform()
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

    def choose_switch(self):
        self.Driver.wait_and_click(self.CHOOSE_SWITCH_PATH.format(self.best_pick()), by=By.XPATH)

    def get_type(self, side, num=0):
        tooltip_div = "//div[contains(@class, 'tooltip tooltip-')]"
        img_ext = "/h2/img[@class='pixelated'][@height='14']"
        types = []
        if side == self.SELF_SIDE:
            self.Driver.wait_for_element(self.ACTIVE_POKE_PATH, by=By.XPATH)
            if num == 1:
                poke_elem = self.Driver.driver.find_element(value=self.ACTIVE_POKE_PATH, by=By.XPATH)
            else:
                poke_elem = self.Driver.driver.find_element(value=self.CHOOSE_SWITCH_PATH.format(num), by=By.XPATH)
        else:
            self.Driver.wait_for_element("//div[contains(@class, 'statbar lstatbar')]/strong", by=By.XPATH)
            poke_elem = self.Driver.driver.find_element(value=self.OPP_POKE_PATH, by=By.XPATH)
        self.AC.move_to_element(poke_elem).perform()
        self.Driver.wait_for_element(tooltip_div, by=By.XPATH)
        self.Driver.wait_for_element(tooltip_div + img_ext, by=By.XPATH)
        poke_types = self.Driver.driver.find_elements(value=tooltip_div + img_ext, by=By.XPATH)
        for t in poke_types:
            types.append(t.get_attribute('alt'))
        return types

    def get_ability_item(self, side, num=0):
        if side == self.SELF_SIDE:
            if num == 0:
                poke_elem = self.Driver.driver.find_element(value=self.ACTIVE_POKE_PATH, by=By.XPATH)
            else:
                poke_elem = self.Driver.driver.find_element(value=self.CHOOSE_SWITCH_PATH.format(num), by=By.XPATH)
            self.AC.move_to_element(poke_elem).perform()
            self.Driver.wait_for_element("div[class='tooltip tooltip-switchpokemon']", by=By.CSS_SELECTOR)
            # Get Pokemon ability
            temp_elm = self.Driver.driver.find_element(value="//*[contains(text(), 'Ability:')]", by=By.XPATH)
            ability_item = temp_elm.find_element(value='./..', by=By.XPATH).text.replace('Ability: ', '').split('/')
            ability = ability_item[0].strip()
            item = ability_item[1].strip().replace('Item: ', '')
            if 'None' in item:
                for m in util.ITEM_REGEX:
                    if match(m, item):
                        item = sub(m, '\1', item)
                        break
            return ability, item
        else:
            self.AC.move_to_element(self.Driver.driver.find_element(value=self.OPP_POKE_PATH, by=By.XPATH)).perform()
            self.Driver.wait_for_element("div[class='tooltip tooltip-activepokemon']", by=By.CSS_SELECTOR)
            # Get abilities
            temp_elm = self.Driver.driver.find_element(
                value="//small[contains(text(), 'bilit')][contains(text(), ':')]", by=By.XPATH)
            if 'Ability' in temp_elm.text:
                # Ability known
                abilities = [temp_elm.find_element(value='./..', by=By.XPATH).text.replace('Ability: ', '').strip()]
            else:
                # Possible abilities
                abilities = temp_elm.find_element(value='./..', by=By.XPATH).text.split(':')[1].strip().split(', ')
            temp_elm = self.Driver.driver.find_elements(value="//small[contains(text(), 'Item:')]", by=By.XPATH)
            if len(temp_elm) > 0:
                item = temp_elm[0].find_element(value='./..', by=By.XPATH).text.replace('Item: ', '').strip()
                if 'None' in item:
                    for m in util.ITEM_REGEX:
                        if match(m, item):
                            item = sub(m, '\1', item)
                            break
            else:
                item = ''
            return abilities, item

    # TODO Update for team
    def get_stats(self, num=0):
        tooltip_div = "//div[contains(@class, 'tooltip tooltip-')]"
        self.Driver.wait_for_element(self.ACTIVE_POKE_PATH, by=By.XPATH)
        poke_elem = self.Driver.driver.find_element(value="//div[@class='has-tooltip'][@data-id='p1a']", by=By.XPATH)
        self.AC.move_to_element(poke_elem).perform()
        self.Driver.wait_for_element(tooltip_div, by=By.XPATH)
        temp_elm = self.Driver.driver.find_elements(value=tooltip_div + "/p/*[contains(text(), 'Atk')]", by=By.XPATH)
        if len(temp_elm) > 1:
            after_elem = self.Driver.driver.find_element(
                value=tooltip_div + "/p/*[contains(text(), '(After stat modifiers:)')]", by=By.XPATH)
            stats = after_elem.find_element(value='./../following-sibling::p', by=By.XPATH)
        elif len(temp_elm) == 0:
            return {}
        else:
            stats = temp_elm[0].find_element(value='./..', by=By.XPATH)
        stats_text = stats.text.split(' / ')
        stats_dict = {}
        for s in stats_text:
            vals = s.split(' ')
            stats_dict[vals[0]] = float(vals[1])
        return stats_dict

    def get_item(self, side):
        pass

    @staticmethod
    def damage_calc(player_types, move, opponent_types, ability, item, stats):
        dmg = move.base_power
        if move.type == util.IMMUNE_ABILITIES.get(ability, None):
            dmg *= 0.0
        if move.type in player_types:
            dmg *= 1.5
        if ability == 'Wonder Guard':
            hit = False
            for t in opponent_types:
                hit = util.type_effectiveness(move.type, t) == 2.0 or hit
                if not hit:
                    dmg *= 0
        for t in opponent_types:
            dmg *= util.type_effectiveness(move.type, t)
        if item == 'Air Balloon' and move.type == util.GROUND:
            dmg *= 0
        if move.move_type == util.PHYSICAL:
            dmg *= stats.get(util.ATK, 1.0)
        elif move.move_type == util.SPECIAL:
            dmg *= stats.get(util.SPA, 1.0)
        return dmg

    def choose_action(self):
        pass

    def best_pick(self):
        pass
