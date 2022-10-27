import os
from os.path import exists
from re import match, search, sub

from selenium.common import NoSuchElementException
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

    def __init__(self, bot, headless):
        self.bot = bot
        self.headless = headless
        self.known_move_map, self.abilities_map, self.move_map, self.stats_map = {}, {}, {}, {}
        self.abilities_list, self.item_list = [], []
        self.updated_known_moves, self.updated_abilities, self.updated_move_info = False, False, False
        self.updated_abilities_list, self.updated_item_list = False, False
        self.load_data(util.KNOWN_MOVES_FILE), self.load_data(util.KNOWN_ABILITIES_FILE)
        self.load_data(util.MOVES_FILE), self.load_data(util.STATS_FILE), self.load_data(util.ABILITIES_FILE)
        self.load_data(util.ITEMS_FILE)
        self.turn = 0
        self.self_team, self.opp_team = [], []
        self.battle_info = []
        self.player_toxic_num, self.opp_toxic_num = 0, 0
        self.player_last_toxic_turn, self.opp_last_toxic_turn = 0, 0
        self.player_alive, self.opp_alive = 6, 6

    def reset(self):
        self.turn = 0
        self.self_team, self.opp_team = [], []
        self.battle_info = []
        self.updated_known_moves, self.updated_abilities, self.updated_move_info = False, False, False
        self.updated_abilities_list, self.updated_item_list = False, False
        self.player_toxic_num, self.opp_toxic_num = 0, 0
        self.player_last_toxic_turn, self.opp_last_toxic_turn = 0, 0
        self.player_alive, self.opp_alive = 6, 6

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
                    if file_type == util.ABILITIES_FILE:
                        self.abilities_list.append(line.rstrip())
                    if file_type == util.ITEMS_FILE:
                        self.item_list.append(line.rstrip())
                    data = line.rstrip().split(',')
                    if file_type == util.KNOWN_MOVES_FILE:
                        self.known_move_map[data[0]] = data[1:]
                    if file_type == util.KNOWN_ABILITIES_FILE:
                        self.abilities_map[data[0]] = data[1:]
                    if file_type == util.MOVES_FILE:
                        if len(data) < 5:
                            self.move_map[data[0]] = Move(*data)
                        else:
                            self.move_map[data[0]] = Move(data[0], data[1], data[2], float(data[3]), data[4:])
                    if file_type == util.STATS_FILE:
                        self.stats_map[data[0]] = data[1:]

    def update_data(self, info_type, poke, data):
        known = self.known_move_map.get(poke, []) if info_type == self.MOVE_INFO else self.abilities_map.get(poke, [])
        updated = False
        for d in data:
            if d not in known and d != '' and d != util.ILLUSION_MSG:
                known.append(d)
                if info_type == self.MOVE_INFO:
                    self.updated_known_moves = True
                else:
                    self.updated_abilities = True
                    if d not in self.abilities_list:
                        self.abilities_list.append(d)
                        self.abilities_list.sort()
                        self.updated_abilities_list = True
                updated = True
        if info_type == self.MOVE_INFO and updated:
            self.known_move_map[poke] = known
        elif info_type == self.ABILITY_INFO and updated:
            self.abilities_map[poke] = known

    def update_item_list(self, item):
        if '(' in item:
            item = item.split('(')[0].strip()
        if item not in self.item_list and item != '' and item != '' and item != 'None':
            self.item_list.append(item)
            self.item_list.sort()
            self.updated_item_list = True

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
            with open(util.KNOWN_ABILITIES_FILE, 'w', encoding='cp1252') as f:
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
        if self.updated_abilities_list:
            with open(util.ABILITIES_FILE, 'w', encoding='cp1252') as f:
                lines = ''
                for a in self.abilities_list:
                    lines += '{}\n'.format(a)
                f.write(lines)
        if self.updated_item_list:
            with open(util.ITEMS_FILE, 'w', encoding='cp1252') as f:
                lines = ''
                for i in self.item_list:
                    lines += '{}\n'.format(i)
                f.write(lines)
        with open(util.STATS_FILE, 'w', encoding='cp1252') as f:
            lines = ''
            for poke in self.stats_map:
                lines += '{},{}\n'.format(poke, ','.join(self.stats_map[poke]))
            f.write(lines)
        if not self.headless:
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
                        stats.append(str(round(float(p.stats[s]), 1)))
            else:
                for s in util.STATS_LIST:
                    stats.append(str(round(float(p.stats[s]), 1)))
            self.stats_map[p.name] = stats

    def translate_log(self, Driver, msg, regex):
        if not Driver.in_battle():
            log_msg(msg, regex)
        try:
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
                    if text == util.TOX:
                        if self.opp_last_toxic_turn == self.turn - 1:
                            self.opp_toxic_num += 1
                        else:
                            self.opp_toxic_num = 1
                        dmg = min(93.75, 6.25 * self.opp_toxic_num)
                        self.opp_last_toxic_turn = self.turn
                        log_msg(msg, regex).replace('poison dmg', '-{}% health'.format(dmg))
                    elif text == util.PSN:
                        return log_msg(msg, regex).replace('poison dmg', '-12.5% health')
            if regex == util.PLAYER_POISON and not player_fainted:
                status_xpath = "//div[@class='statbar rstatbar']/div[@class='hpbar']/div[@class='status']/*"
                stat_changes = Driver.driver.find_elements(value=status_xpath, by=By.XPATH)
                for s in stat_changes:
                    text = s.text
                    if text == util.TOX:
                        if self.player_last_toxic_turn == self.turn - 1:
                            self.player_toxic_num += 1
                        else:
                            self.player_toxic_num = 1
                        dmg = min(93.75, 6.25 * self.player_toxic_num)
                        self.player_last_toxic_turn = self.turn
                        log_msg(msg, regex).replace('poison dmg', '-{}% health'.format(dmg))
                    elif text == util.PSN:
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
                field = Driver.get_field_settings(Driver.SELF_SIDE)
                num = (2.080 * (field[util.FIELD_SPIKES] ^ 2)) - (2.07 * field[util.FIELD_SPIKES]) + 12.49
                return log_msg(msg, regex).replace('spike dmg', '-{}% health'.format(num))
            if regex == util.PLAYER_SPIKE_DMG and not player_fainted:
                field = Driver.get_field_settings(Driver.OPP_SIDE)
                num = (2.080 * (field[util.FIELD_SPIKES] ^ 2)) - (2.07 * field[util.FIELD_SPIKES]) + 12.49
                return log_msg(msg, regex).replace('spike dmg', '-{}% health'.format(num))
            if regex == util.OPPONENT_WISH:
                name = Driver.driver.find_element(value="//div[contains(@class, 'statbar lstatbar')]/strong",
                                                  by=By.XPATH).text
                return log_msg(msg, regex).replace('active', name)
            if regex == util.PLAYER_WISH:
                name = Driver.driver.find_element(value="//div[contains(@class, 'statbar rstatbar')]/strong",
                                                  by=By.XPATH).text
                return log_msg(msg, regex).replace('active', name)
        except NoSuchElementException:
            pass
        return log_msg(msg, regex)

    def log_turn(self, Driver):
        if self.headless:
            return
        if self.turn == 0:
            elem_path = "//div[@class='battle-history']"
        else:
            elem_path = "//h2[@class='battle-history'][text()='Turn {}']/following-sibling::div[" \
                        "@class='battle-history'] "
        self.battle_info.append('Turn {}'.format(self.turn))
        turn_elems = Driver.driver.find_elements(value=elem_path.format(self.turn), by=By.XPATH)
        for e in turn_elems:
            msg = str(e.text.replace('\n', ''))
            # TODO Record ELO
            if match(util.WIN_MSG, msg):
                if search(util.WIN_MSG, msg).group(1) == Driver.botName:
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
            if msg != '':
                print('NEW MESSAGE:', msg)

    def battle_win(self, Driver):
        # TODO Find alt mode for headless. Problem is that skip removes the win msg
        if self.turn == 0:
            elem_path = "//div[@class='battle-history']"
        else:
            elem_path = "//h2[@class='battle-history'][text()='Turn {}']/following-sibling::div[" \
                        "@class='battle-history'] "
        turn_elems = Driver.driver.find_elements(value=elem_path.format(self.turn), by=By.XPATH)
        for e in turn_elems:
            msg = str(e.text.replace('\n', ''))
            if match(util.WIN_MSG, msg):
                if search(util.WIN_MSG, msg).group(1) == Driver.botName:
                    return True
                else:
                    return False

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
    class Effects:

        def __init__(self, effects):
            self.effects_list = effects
            # TODO Cleanup
            self.priority = 0
            self.tailwind = False
            self.stat_change = []  # Format: List of (Stat[str], Target[str], Amount[int], Chance[bool])
            self.status = None  # Format: (Status[str], Target[str], Chance[bool])
            self.flinch, self.crit = None, None  # Format: Chance[bool]
            self.switch = None  # Format: Target[str]
            self.field = None  # Format: Field[str]
            self.weather = None
            self.counter = None  # Format: Type[str]
            self.dmgheal = None  # Format: Percent[int]
            self.heal = None  # Format: (Target[str], Percent[int], Chance[bool])
            self.recoil = None  # Format: Percent[int]
            self.cure = None  # Format: Target[str]
            self.protect = False
            self.charge, self.recharge = False, False
            self.terrain = None
            self.item_remove = False
            self.rdm_move = False
            self.pain_split = False
            self.contact_dmg = False
            self.trick = False
            self.move_lock = False
            self.levitate = False
            self.lvl_dmg = False
            self.endeavor = False
            self.copycat = False
            self.type_change = None
            self.perish_song = False
            self.transform = False
            if effects is not None:
                for e in effects:
                    if util.PRIORITY in e:
                        self.priority = int(e.split(' ')[1])
                    elif util.COUNTER in e:
                        self.counter = e.split(' ')[1]
                    elif any((stat := s) in e for s in util.STATS_LIST):
                        info = e.split(' ')
                        self.stat_change.append((stat, info[0], int(info[2]), util.CHANCE in e))
                    elif util.STAT_STEAL in e:
                        self.stat_change.append(util.STAT_STEAL)
                    elif util.STATS_CLEAR in e:
                        self.stat_change.append((util.STATS_CLEAR, e.split(' ')[1]))
                    elif any((status := s) in e for s in util.STATUS_LIST):
                        info = e.split(' ')
                        self.status = (status, info[0], util.CHANCE in e)
                    elif util.CONFUSED in e:
                        info = e.split(' ')
                        self.status = (util.CONFUSED, info[0], util.CHANCE in e)
                    elif util.DISABLE in e:
                        info = e.split(' ')
                        if len(info) > 1:
                            self.status = (util.DISABLE, 'Opp', info[1])
                        else:
                            self.status = (util.DISABLE, 'Opp')
                    elif any((status := s) in e for s in [util.ENCORE, util.INFESTATION]):
                        self.status = (status, 'Opp')
                    elif util.FLINCH in e:
                        self.flinch = util.CHANCE in e
                    elif util.CRIT in e:
                        self.crit = util.CHANCE in e
                    elif util.SWITCH in e:
                        self.switch = e.split(' ')[0]
                    elif any((field := f) in e for f in util.FIELD_LIST + [util.FIELD_CLEAR, util.SCREEN_CLEAR,
                                                                           util.LEECH_SEED, util.W_TRICK_ROOM,
                                                                           util.W_TAILWIND]):
                        self.field = field
                    elif any((weather := w) in e for w in util.WEATHER_LIST):
                        self.weather = weather
                    elif util.DMG_HEAL in e:
                        self.dmgheal = int(e.split(' ')[1])
                    elif util.HEAL in e:
                        info = e.split(' ')
                        self.heal = (info[0], int(info[2]), util.CHANCE in e)
                    elif util.RECOIL in e:
                        self.recoil = int(e.split(' ')[1])
                    elif util.CURE in e:
                        self.cure = e.split(' ')[1]
                    elif util.PROTECT in e:
                        self.protect = True
                    elif util.RECHARGE in e:
                        self.recharge = True
                    elif util.CHARGE in e:
                        self.charge = True
                    elif any((terrain := t) in e for t in util.TERRAIN_LIST + [util.TERRAIN_CLEAR]):
                        self.terrain = terrain
                    elif util.ITEM_REMOVE in e:
                        self.item_remove = True
                    elif util.RDM_MOVE in e:
                        self.rdm_move = True
                    elif util.PAINSPLIT in e:
                        self.pain_split = True
                    elif util.CONTACT_DMG in e:
                        self.contact_dmg = True
                    elif util.TRICK in e:
                        self.trick = True
                    elif util.MOVE_LOCK in e:
                        self.move_lock = True
                    elif util.LEVITATE in e:
                        self.levitate = True
                    elif util.LVL_DMG in e:
                        self.lvl_dmg = True
                    elif util.ENDEAVOR in e:
                        self.endeavor = True
                    elif util.COPYCAT in e:
                        self.copycat = True
                    elif util.TYPE_CHANGE in e:
                        info = e.split(' ')
                        self.type_change = (info[1], info[2])
                    elif util.PERISHSONG in e:
                        self.perish_song = True
                    elif util.TRANSFORM in e:
                        self.transform = True
                    else:
                        print(e)

        def __repr__(self):
            return ','.join(self.effects_list)

    def __init__(self, name="", t=util.UNKNOWN, move_type=util.STATUS, base_power=0.0, effects=None):
        self.name = name
        self.type = t
        self.move_type = move_type
        self.base_power = float(base_power)
        if effects is not None:
            self.effects = self.Effects(effects)
        else:
            self.effects = None

    def __repr__(self):
        if self.effects is not None:
            return ','.join([self.name, self.type, self.move_type, str(self.base_power), repr(self.effects)])
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
