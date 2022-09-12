from os.path import exists

from selenium.webdriver.common.by import By

MOVES_FILE, ABILITIES_FILE = './data/moves.data', './data/abilities.data'


class BattleLogger:
    MOVE_INFO, ABILITY_INFO = 0, 1

    def __init__(self):
        self.known_move_map, self.abilities_map = {}, {}
        self.updated_moves, self.updated_abilities = False, False
        self.load_data(MOVES_FILE), self.load_data(ABILITIES_FILE)
        self.turn = 0

    def load_data(self, file_type):
        if exists(file_type):
            with open(file_type) as f:
                for line in f:
                    data = line.rstrip().split(',')
                    if file_type == MOVES_FILE:
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
            with open(MOVES_FILE, 'w') as f:
                lines = ''
                for poke in self.known_move_map:
                    lines += '{},{}\n'.format(poke, ','.join(self.known_move_map[poke]))
                f.write(lines)
        if self.updated_abilities:
            with open(ABILITIES_FILE, 'w') as f:
                lines = ''
                for poke in self.abilities_map:
                    lines += '{},{}\n'.format(poke, ','.join(self.abilities_map[poke]))
                f.write(lines)

    def log_turn(self, Driver):
        elem_path = "//h2[@class='battle-history'][text()='Turn {}']/following-sibling::div[@class='battle-history']"
        turn_elems = Driver.driver.find_elements(value=elem_path.format(self.turn), by=By.XPATH)
        for e in turn_elems:
            # TODO
            pass
