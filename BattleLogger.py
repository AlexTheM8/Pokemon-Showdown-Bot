from os.path import exists
from re import match, sub

from selenium.webdriver.common.by import By

import util


# TODO Translate to logs
def log_msg(msg, regex):
    replace = r''
    for i in range(util.MSG_DICT[regex].count('{}')):
        replace += r'\{}|'.format(i+1)
    args = sub(regex, replace, msg)
    print(util.MSG_DICT[regex].format(*(args.split('|')[:-1])))


class BattleLogger:
    MOVE_INFO, ABILITY_INFO = 0, 1

    def __init__(self):
        self.known_move_map, self.abilities_map = {}, {}
        self.updated_moves, self.updated_abilities = False, False
        self.load_data(util.MOVES_FILE), self.load_data(util.ABILITIES_FILE)
        self.turn = 0

    def load_data(self, file_type):
        if exists(file_type):
            with open(file_type) as f:
                for line in f:
                    data = line.rstrip().split(',')
                    if file_type == util.MOVES_FILE:
                        self.known_move_map[data[0]] = data[1:]
                    else:
                        self.abilities_map[data[0]] = data[1:]

    def update_data(self, info_type, poke, data):
        known = self.known_move_map.get(poke, []) if info_type == self.MOVE_INFO else self.abilities_map.get(poke, [])
        updated = False
        for d in data:
            if d not in known:
                known.append(d)
                if info_type == self.MOVE_INFO:
                    self.updated_moves = True
                else:
                    self.updated_abilities = True
                updated = True
        if info_type == self.MOVE_INFO and updated:
            self.known_move_map[poke] = known
        elif info_type == self.ABILITY_INFO and updated:
            self.abilities_map[poke] = known

    def save_data(self):
        if self.updated_moves:
            with open(util.MOVES_FILE, 'w') as f:
                lines = ''
                for poke in self.known_move_map:
                    lines += '{},{}\n'.format(poke, ','.join(self.known_move_map[poke]))
                f.write(lines)
        if self.updated_abilities:
            with open(util.ABILITIES_FILE, 'w') as f:
                lines = ''
                for poke in self.abilities_map:
                    lines += '{},{}\n'.format(poke, ','.join(self.abilities_map[poke]))
                f.write(lines)

    def log_turn(self, Driver):
        if self.turn == 0:
            elem_path = "//div[@class='battle-history']"
        else:
            elem_path = "//h2[@class='battle-history'][text()='Turn {}']/following-sibling::div[@class='battle-history']"
        turn_elems = Driver.driver.find_elements(value=elem_path.format(self.turn), by=By.XPATH)
        for e in turn_elems:
            msg = e.text.replace('\n', '')
            # TODO Translate to logs
            # Switch-case on logs
            found_match = False
            for r in util.REGEX_LIST:
                if match(r, msg):
                    log_msg(msg, r)
                    found_match = True
                    break
            if not found_match:
                for r in util.IGNORE_LIST:
                    if match(r, msg):
                        found_match = True
                        break
            if not found_match:
                print('NEW MESSAGE:', msg)
