from os.path import exists
from re import match, sub

from selenium.webdriver.common.by import By

MOVES_FILE, ABILITIES_FILE = './data/moves.data', './data/abilities.data'

# Regex Log Messages
OPPONENT_MOVE = r'^The opposing.*used.*!$'
PLAYER_MOVE = r'^.*used.*!$'
OPPONENT_DAMAGE = r'^(The opposing.*lost.*of its health!)$'
PLAYER_DAMAGE = r'^(.*lost.*of its health!)$'
OPPONENT_STATUS_DROP = r'^The opposing.*\'s.*fell!$'
PLAYER_STATUS_DROP = r'^.*\'s.*fell!$'
OPPONENT_SWITCH_1 = r'^.*withdrew.*!$'
OPPONENT_SWITCH_2 = r'^The opposing.*went back to.*!$'
OPPONENT_SELECT = r'^.*sent out.*!$'
OPPONENT_MEGA = r'^The opposing.*has Mega Evolved into.*!$'
OPPONENT_RECOIL = r'^The opposing.*was damaged by the recoil!$'
OPPONENT_FAINT = r'^The opposing.*fainted!$'
PLAYER_FAINT = r'^.*fainted!$'


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
            msg = e.text
            # TODO Translate to logs
            # Switch-case on logs
            if match(OPPONENT_MOVE, msg):
                msg = msg.replace('The opposing ', '')
                poke = msg.split(' used ')[0]
                move = msg.split(' used ')[1].replace('!', '')
                print('Opponent {} used {}'.format(poke, move))
            elif match(PLAYER_MOVE, msg):
                poke = msg.split(' used ')[0]
                move = msg.split(' used ')[1].replace('!', '')
                print('Player {} used {}'.format(poke, move))
            elif match(OPPONENT_DAMAGE, msg):
                msg = msg.replace('(The opposing ', '')
                poke = msg.split(' lost ')[0]
                dmg = msg.split(' lost ')[1].replace(' of its health!)', '')
                print('Opponent {} lost {} health'.format(poke, dmg))
            elif match(PLAYER_DAMAGE, msg):
                poke = msg.split(' lost ')[0].replace('(', '')
                dmg = msg.split(' lost ')[1].replace(' of its health!)', '')
                print('Player {} lost {} health'.format(poke, dmg))
            elif match(OPPONENT_DAMAGE, msg):
                msg = msg.replace('The opposing ', '')
                poke = msg.split('\'s ')[0]
                stat = msg.split('\'s ')[1].replace(' fell!', '')
                print('Opponent {} {} down'.format(poke, stat))
            elif match(PLAYER_DAMAGE, msg):
                poke = msg.split('\'s ')[0]
                stat = msg.split('\'s ')[1].replace(' fell!', '')
                print('Player {} {} down'.format(poke, stat))
            elif match(OPPONENT_SWITCH_1, msg) or match(OPPONENT_SWITCH_2, msg):
                if match(OPPONENT_SWITCH_1, msg):
                    poke = ''.join(msg.split(' ')[2:]).replace('!', '')
                    print('Opponent withdrew {}'.format(poke))
                else:
                    msg = msg.replace('The opposing ', '')
                    poke = msg.split(' went back to')[0]
                    print('Opponent withdrew {}'.format(poke))
            elif match(OPPONENT_SELECT, msg):
                poke = msg.split('sent out ')[1].replace('!', '')
                print('Opponent chose {}'.format(poke))
            elif match(OPPONENT_MEGA, msg):
                msg = msg.replace('The opposing ', '')
                poke = msg.split(' has Mega Evolved')[0]
                mega = msg.split('Mega Evolved into ')[1].replace('!', '')
                print('Opponent {} mega evolved to {}'.format(poke, mega))
            elif match(OPPONENT_RECOIL, msg):
                poke = sub(OPPONENT_RECOIL, '', msg).strip()
                print('Opponent {} recoiled'.format(poke))
            elif match(OPPONENT_FAINT, msg):
                poke = sub(OPPONENT_FAINT, '', msg).strip()
                print('Opponent {} fainted'.format(poke))
            elif match(PLAYER_FAINT, msg):
                poke = sub(PLAYER_FAINT, '', msg).strip()
                print('Player {} fainted'.format(poke))
            else:
                print('NEW MESSAGE: ', msg)
            # TODO NOTES
            '''             
            Sylveon avoided the attack!
            
            Sylveon restored a little HP using its Leftovers!
            
            Sylveon, come back!
                Go! Cinccino!
                
            The opposing Thundurus put in a substitute!
            
            The substitute took damage for the opposing Thundurus!
            
            Dusknoir frisked the opposing Conkeldurr and found its Life Orb!
            
            The opposing Conkeldurr was burned!
            
            The opposing Conkeldurr knocked off Dusknoir's Leftovers!
            
            The opposing Conkeldurr lost some of its HP!
            
            (Since gen 7, Dark is immune to Prankster moves.)
            
            It doesn't affect the opposing Incineroar...
            
            The opposing Zapdos was seeded!
            
            The opposing Zapdos's health is sapped by Leech Seed!
            
            The Pokémon was hit 2 times!
            
            [The opposing Incineroar's Intimidate]
            
            The opposing Giratina's Sp. Atk fell harshly!
            '''
