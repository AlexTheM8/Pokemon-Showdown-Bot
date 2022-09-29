from os.path import exists
from re import match, sub

from selenium.webdriver.common.by import By

import util


# TODO Translate to logs
def log_msg(msg, regex):
    replace = r''
    for i in range(util.MSG_DICT[regex].count('{}')):
        replace += r'\{}|'.format(i + 1)
    args = sub(regex, replace, msg)
    print(util.MSG_DICT[regex].format(*(args.split('|')[:-1])))


class BattleLogger:
    MOVE_INFO, ABILITY_INFO = 0, 1

    def __init__(self):
        self.known_move_map, self.abilities_map, self.move_map = {}, {}, {}
        self.updated_known_moves, self.updated_abilities, self.updated_move_info = False, False, False
        self.load_data(util.KNOWN_MOVES_FILE), self.load_data(util.ABILITIES_FILE), self.load_data(util.MOVES_FILE)
        self.turn = 0
        self.self_team, self.opp_team = [], []
        self.battle_info = []

    def reset(self):
        self.turn = 0
        self.updated_known_moves, self.updated_abilities, self.updated_move_info = False, False, False

    def load_data(self, file_type):
        if exists(file_type):
            with open(file_type, encoding='cp1252') as f:
                for line in f:
                    data = line.rstrip().split(',')
                    if file_type == util.KNOWN_MOVES_FILE:
                        self.known_move_map[data[0]] = data[1:]
                    elif file_type == util.ABILITIES_FILE:
                        self.abilities_map[data[0]] = data[1:]
                    else:
                        self.move_map[data[0]] = Move(*data)

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

    def log_turn(self, Driver):
        if self.turn == 0:
            elem_path = "//div[@class='battle-history']"
        else:
            elem_path = "//h2[@class='battle-history'][text()='Turn {}']/following-sibling::div[@class='battle-history']"
        turn_elems = Driver.driver.find_elements(value=elem_path.format(self.turn), by=By.XPATH)
        for e in turn_elems:
            msg = e.text.replace('\n', '')
            found_match = False
            for r in util.REGEX_LIST:
                if match(r, msg):
                    # log_msg(msg, r)
                    found_match = True
                    break
            if not found_match:
                for r in util.IGNORE_LIST:
                    if match(r, msg):
                        found_match = True
                        break
            if not found_match:
                print('NEW MESSAGE:', msg)

    def save_battle_info(self):
        pass


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
        if moves is None:
            moves = []
            for _ in range(4):
                moves.append(Move())
