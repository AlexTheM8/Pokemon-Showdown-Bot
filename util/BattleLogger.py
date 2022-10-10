import os
from os.path import exists
from re import match, sub

from selenium.webdriver.common.by import By

import util.util as util


# TODO Update data (& logs) to parquet files
def log_msg(msg, regex):
    replace = r''
    for i in range(util.MSG_DICT[regex].count('{}')):
        replace += r'\{}|'.format(i + 1)
    args = sub(regex, replace, msg)
    return util.MSG_DICT[regex].format(*(args.split('|')[:-1]))


class BattleLogger:
    MOVE_INFO, ABILITY_INFO = 0, 1

    def __init__(self, bot):
        self.bot = bot
        self.known_move_map, self.abilities_map, self.move_map, self.stats_map = {}, {}, {}, {}
        self.updated_known_moves, self.updated_abilities, self.updated_move_info = False, False, False
        self.load_data(util.KNOWN_MOVES_FILE), self.load_data(util.ABILITIES_FILE), self.load_data(util.MOVES_FILE)
        self.load_data(util.STATS_FILE)
        self.turn = 0
        self.self_team, self.opp_team = [], []
        self.battle_info = []
        self.player_toxic_num, self.opp_toxic_num = 0, 0
        self.player_last_toxic_turn, self.opp_last_toxic_turn = 0, 0

    def reset(self):
        self.turn = 0
        self.self_team, self.opp_team = [], []
        self.battle_info = []
        self.updated_known_moves, self.updated_abilities, self.updated_move_info = False, False, False
        self.player_toxic_num, self.opp_toxic_num = 0, 0
        self.player_last_toxic_turn, self.opp_last_toxic_turn = 0, 0

    def update_opp_team(self, poke):
        if not any(poke.name == p.name for p in self.opp_team):
            self.opp_team.append(poke)
        else:
            for i, p in enumerate(self.opp_team):
                if p.name == poke.name:
                    self.opp_team[i] = poke
                    break

    def load_data(self, file_type):
        if exists(file_type):
            with open(file_type, encoding='cp1252') as f:
                for line in f:
                    data = line.rstrip().split(',')
                    if file_type == util.KNOWN_MOVES_FILE:
                        self.known_move_map[data[0]] = data[1:]
                    elif file_type == util.ABILITIES_FILE:
                        self.abilities_map[data[0]] = data[1:]
                    elif file_type == util.MOVES_FILE:
                        self.move_map[data[0]] = Move(*data)
                    else:
                        self.stats_map[data[0]] = data[1:]

    def update_data(self, info_type, poke, data):
        known = self.known_move_map.get(poke, []) if info_type == self.MOVE_INFO else self.abilities_map.get(poke, [])
        updated = False
        for d in data:
            if d not in known and d != '':
                known.append(d)
                if info_type == self.MOVE_INFO:
                    self.updated_known_moves = True
                else:
                    self.updated_abilities = True
                updated = True
        if info_type == self.MOVE_INFO and updated:
            self.known_move_map[poke] = known
        elif info_type == self.ABILITY_INFO and updated:
            self.abilities_map[poke] = known

    def update_move_info(self, move):
        if move.name not in self.move_map.keys():
            self.move_map[move.name] = move
            self.updated_move_info = True

    def save_data(self):
        if self.updated_known_moves:
            with open(util.KNOWN_MOVES_FILE, 'w', encoding='cp1252') as f:
                lines = ''
                for poke in self.known_move_map:
                    lines += '{},{}\n'.format(poke, ','.join(self.known_move_map[poke]))
                f.write(lines)
        if self.updated_abilities:
            with open(util.ABILITIES_FILE, 'w', encoding='cp1252') as f:
                lines = ''
                for poke in self.abilities_map:
                    lines += '{},{}\n'.format(poke, ','.join(self.abilities_map[poke]))
                f.write(lines)
        if self.updated_move_info:
            with open(util.MOVES_FILE, 'w', encoding='cp1252') as f:
                lines = ''
                for move in self.move_map:
                    lines += repr(self.move_map[move]) + '\n'
                f.write(lines)
        with open(util.STATS_FILE, 'w', encoding='cp1252') as f:
            lines = ''
            for poke in self.stats_map:
                lines += '{},{}\n'.format(poke, ','.join(self.stats_map[poke]))
            f.write(lines)
        self.save_battle_info()

    def update_stats(self):
        for p in self.self_team:
            stats = []
            if p.name in self.stats_map:
                for i, s in enumerate(util.STATS_LIST):
                    if float(p.stats[s]) > float(self.stats_map[p.name][i]):
                        stats.append(str(round((float(p.stats[s]) + float(self.stats_map[p.name][i])) / 2.1, 1)))
                    elif float(p.stats[s]) < float(self.stats_map[p.name][i]):
                        stats.append(str(round((float(p.stats[s]) + float(self.stats_map[p.name][i])) / 1.9, 1)))
                    else:
                        stats.append(str(p.stats[s]))
            else:
                for s in util.STATS_LIST:
                    stats.append(str(p.stats[s]))
            self.stats_map[p.name] = stats

    def translate_log(self, Driver, msg, regex):
        if not Driver.in_battle():
            log_msg(msg, regex)
        temp_elem = Driver.driver.find_elements(
            value="//div[@class='trainer trainer-far']/div[@class='teamicons']/span[@class='picon has-tooltip']",
            by=By.XPATH)
        player_fainted = \
            Driver.driver.find_element(value="//button[@name='chooseDisabled'][@data-tooltip='switchpokemon|0']",
                                       by=By.XPATH).get_attribute('value').split(',')[1] == 'fainted'
        opp_fainted = not any('active' in e.get_attribute('aria-label') for e in temp_elem)
        if opp_fainted and player_fainted:
            return log_msg(msg, regex)
        if regex == util.OPPONENT_POISON and not opp_fainted:
            status_xpath = "//div[@class='statbar lstatbar']/div[@class='hpbar']/div[@class='status']/*"
            stat_changes = Driver.driver.find_elements(value=status_xpath, by=By.XPATH)
            for s in stat_changes:
                text = s.text
                if text == 'TOX':
                    if self.opp_last_toxic_turn == self.turn - 1:
                        self.opp_toxic_num += 1
                    else:
                        self.opp_toxic_num = 1
                    dmg = min(93.75, 6.25 * self.opp_toxic_num)
                    self.opp_last_toxic_turn = self.turn
                    log_msg(msg, regex).replace('poison dmg', '-{}% health'.format(dmg))
                elif text == 'PSN':
                    return log_msg(msg, regex).replace('poison dmg', '-12.5% health')
        if regex == util.PLAYER_POISON and not player_fainted:
            status_xpath = "//div[@class='statbar rstatbar']/div[@class='hpbar']/div[@class='status']/*"
            stat_changes = Driver.driver.find_elements(value=status_xpath, by=By.XPATH)
            for s in stat_changes:
                text = s.text
                if text == 'TOX':
                    if self.player_last_toxic_turn == self.turn - 1:
                        self.player_toxic_num += 1
                    else:
                        self.player_toxic_num = 1
                    dmg = min(93.75, 6.25 * self.player_toxic_num)
                    self.player_last_toxic_turn = self.turn
                    log_msg(msg, regex).replace('poison dmg', '-{}% health'.format(dmg))
                elif text == 'PSN':
                    return log_msg(msg, regex).replace('poison dmg', '-12.5% health')
        if regex == util.OPPONENT_STONE_DMG and not opp_fainted:
            types = Driver.get_type(Driver.OPP_SIDE)
            effectiveness = 12.5
            for t in types:
                effectiveness *= util.type_effectiveness(util.ROCK, t)
            return log_msg(msg, regex).replace('stone dmg', '-{}% health'.format(effectiveness))
        if regex == util.PLAYER_STONE_DMG and not player_fainted:
            types = Driver.get_type(Driver.SELF_SIDE)
            effectiveness = 12.5
            for t in types:
                effectiveness *= util.type_effectiveness(util.ROCK, t)
            return log_msg(msg, regex).replace('stone dmg', '-{}% health'.format(effectiveness))
        if regex == util.OPPONENT_SPIKE_DMG and not opp_fainted:
            base = Driver.driver.find_elements(value="//img[contains(@src, 'caltrop')]/../../*[2]/*", by=By.XPATH)
            num = (2.080 * (len(base) ^ 2)) - (2.07 * len(base)) + 12.49
            return log_msg(msg, regex).replace('spike dmg', '-{}% health'.format(num))
        if regex == util.PLAYER_SPIKE_DMG and not player_fainted:
            base = Driver.driver.find_elements(value="//img[contains(@src, 'caltrop')]/../../*[3]/*", by=By.XPATH)
            num = (2.080 * (len(base) ^ 2)) - (2.07 * len(base)) + 12.49
            return log_msg(msg, regex).replace('spike dmg', '-{}% health'.format(num))
        if regex == util.OPPONENT_WISH:
            name = Driver.driver.find_element(value="//div[contains(@class, 'statbar lstatbar')]/strong",
                                              by=By.XPATH).text
            return log_msg(msg, regex).replace('active', name)
        if regex == util.PLAYER_WISH:
            name = Driver.driver.find_element(value="//div[contains(@class, 'statbar rstatbar')]/strong",
                                              by=By.XPATH).text
            return log_msg(msg, regex).replace('active', name)
        return log_msg(msg, regex)

    def log_turn(self, Driver):
        if self.turn == 0:
            elem_path = "//div[@class='battle-history']"
        else:
            elem_path = "//h2[@class='battle-history'][text()='Turn {}']/following-sibling::div[" \
                        "@class='battle-history'] "
        self.battle_info.append('Turn {}'.format(self.turn))
        turn_elems = Driver.driver.find_elements(value=elem_path.format(self.turn), by=By.XPATH)
        for e in turn_elems:
            msg = e.text.replace('\n', '')
            if match(util.WIN_MSG, msg):
                if sub(util.WIN_MSG, '\1', msg) == Driver.botName:
                    self.battle_info.append('Win\n')
                else:
                    self.battle_info.append('Lose\n')
                continue
            if any(match((reg := r), msg) for r in util.VARIED_RESULT_LIST):
                log = self.translate_log(Driver, msg, reg)
                if log != '':
                    self.battle_info.append(log)
                continue
            if any(match((reg := r), msg) for r in util.REGEX_LIST):
                log = log_msg(msg, reg)
                if log != '':
                    self.battle_info.append(log)
                continue
            if any(match(r, msg) for r in util.IGNORE_LIST):
                continue
            print('NEW MESSAGE:', msg)

    def save_battle_info(self):
        num_files = len(os.listdir(util.LOG_ROOT))
        with open(util.BASE_LOG_FILE.format(num_files), 'w', encoding='cp1252') as f:
            lines = '{}\n'.format(self.bot)
            for poke in self.self_team:
                lines += repr(poke) + '\n'
            lines += '\n'
            for poke in self.opp_team:
                lines += repr(poke) + '\n'
            lines += '\n'
            for line in self.battle_info:
                lines += line + '\n'
            f.write(lines)


class Move:

    def __init__(self, name="", t=util.UNKNOWN, move_type=util.STATUS, base_power=0.0):
        self.name = name
        self.type = t
        self.move_type = move_type
        self.base_power = base_power
        # TODO Effects

    def __repr__(self):
        return ','.join([self.name, self.type, self.move_type, str(self.base_power)])


class Pokemon:

    def __init__(self, name="", ability="", item="", moves=None, stats=None):
        self.moves = moves
        self.name = name
        self.ability = ability
        self.item = item
        self.stats = stats

    def __repr__(self):
        repr_list = [self.name, self.ability, self.item]
        if self.moves is not None:
            repr_list.extend(self.moves)
            if len(self.moves) < 4:
                repr_list.extend([""] * (4 - len(self.moves)))
        else:
            repr_list.extend([""] * 4)
        return ','.join(repr_list)
