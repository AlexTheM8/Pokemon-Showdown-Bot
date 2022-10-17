import glob
import random
from re import findall, match, search

import numpy as np
import tensorflow as tf
from selenium.common import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from tensorflow import keras

from collections import deque
from bots.BattleBot import BattleBot
from util import util

MODEL_CKPT_PATH = './data/models/'
CKPT_FILE = 'checkpoint_{}.ckpt'
MAIN_MODEL, TGT_MODEL = 'main/', 'target/'


def train(replay_memory, model, target_model):
    learning_rate = 0.7  # Learning rate
    discount_factor = 0.618

    MIN_REPLAY_SIZE = 1000
    if len(replay_memory) < MIN_REPLAY_SIZE:
        return

    batch_size = 64 * 2
    mini_batch = random.sample(replay_memory, batch_size)
    current_states = np.array([transition[0] for transition in mini_batch])
    current_qs_list = model.predict(current_states)
    new_current_states = np.array([transition[3] for transition in mini_batch])
    future_qs_list = target_model.predict(new_current_states)

    X = []
    Y = []
    for index, (observation, action, reward, new_observation, done) in enumerate(mini_batch):
        if not done:
            max_future_q = reward + discount_factor * np.max(future_qs_list[index])
        else:
            max_future_q = reward

        current_qs = current_qs_list[index]
        current_qs[action] = (1 - learning_rate) * current_qs[action] + learning_rate * max_future_q

        X.append(observation)
        Y.append(current_qs)
    model.fit(np.array(X), np.array(Y), batch_size=batch_size, verbose=0, shuffle=True)


def by_num(name):
    base, _ = name.split('.')
    _, num = base.split('_')
    return int(num)


def calc_status_change(old, new):
    if old == -1 and new != -1:
        return -10.0
    if old != -1 and new == -1:
        return 10.0
    return 0.0


class NeuralNetBot(BattleBot):

    def __init__(self):
        super().__init__()
        self.epsilon = 1
        self.max_epsilon = 1
        self.min_epsilon = 0.01
        self.decay = 0.001
        self.episode = 0
        self.main_ckpt_num, self.tgt_ckpt_num = 0, 0

        self.state_shape, self.action_shape = (191,), 13
        self.model = self.agent(self.state_shape, self.action_shape, MAIN_MODEL)
        self.tgt_model = self.agent(self.state_shape, self.action_shape, TGT_MODEL)
        if self.main_ckpt_num == 0:
            self.tgt_model.set_weights(self.model.get_weights())

        self.replay_memory = deque(maxlen=50_000)

        self.target_update_counter = 0

        self.steps_to_update_target_model = 0
        self.observation = np.array([])
        self.total_training_rewards = 0

    def battle(self):
        super().battle()
        train(self.replay_memory, self.model, self.tgt_model)
        self.total_training_rewards += 1
        if self.steps_to_update_target_model >= 100:
            self.tgt_model.set_weights(self.model.get_weights())
            self.steps_to_update_target_model = 0
            self.tgt_model.save_weights(''.join([MODEL_CKPT_PATH, TGT_MODEL, CKPT_FILE]).format(self.tgt_ckpt_num))
            self.tgt_ckpt_num += 1
        self.model.save_weights(''.join([MODEL_CKPT_PATH, MAIN_MODEL, CKPT_FILE]).format(self.main_ckpt_num))
        self.main_ckpt_num += 1
        self.epsilon = self.min_epsilon + (self.max_epsilon - self.min_epsilon) * np.exp(-self.decay * self.episode)
        self.episode += 1

    def battle_actions(self):
        try:
            # Check if used switching move
            if not self.Driver.driver.find_elements(value="//div[@class='movemenu']", by=By.XPATH):
                self.choose_action()
                return
            self.battle_logger.log_turn(self.Driver)
            self.read_team(self.Driver.OPP_SIDE)
            if self.battle_logger.turn == 0:
                self.observation = self.get_observation()
            self.choose_action()
            self.battle_logger.turn += 1
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException, ValueError):
            return

    def choose_action(self):
        self.steps_to_update_target_model += 1
        random_number = np.random.rand()
        if random_number <= self.epsilon:
            action_list, has_z, mega_elm = self.limit_actions()
            action = random.choice(action_list)
        else:
            encoded = self.observation
            encoded_reshaped = encoded.reshape([1, encoded.shape[0]])
            predicted = self.model.predict(encoded_reshaped).flatten()
            action_list, has_z, mega_elm = self.limit_actions(predicted)
            action = np.argmax(action_list)
        new_observation, reward, done = self.do_action(action, has_z, mega_elm)
        self.replay_memory.append([self.observation, action, reward, new_observation, done])

        if self.steps_to_update_target_model % 4 == 0:
            train(self.replay_memory, self.model, self.tgt_model)

        self.observation = new_observation
        self.total_training_rewards += reward

    def do_action(self, action, has_z, mega_elm):
        if action < 8:
            if action < 4:
                self.choose_move(str(action + 1), has_z, mega_elm)
            else:
                self.choose_move('z' + str(action - 3), has_z, mega_elm)
        else:
            self.choose_switch(num=str(action - 7))
        done = self.Driver.wait_for_next_turn()
        # TODO Check validity of this
        new_observation = self.observation if done else self.get_observation()
        # TODO Change to win/lose reward
        reward = 1000 if done else self.calculate_reward(new_observation)
        return new_observation, reward, done

    def limit_actions(self, action_list=None):
        options, has_z, mega_elm = self.move_options()
        if has_z:
            moves, z_moves = [], []
            for v, _ in options:
                if 'z' in v:
                    translation = int(v.replace('z', '')) + 4
                    z_moves.append(translation)
                else:
                    moves.append(v)
            legal_actions = moves + z_moves
        else:
            legal_actions = [int(v) for v, _ in options]
        legal_actions = legal_actions + [int(p) + 8 for p in self.party_options()]
        if action_list is None:
            # Random
            action_list = [x for x in range(1, 14) if x in legal_actions]
        else:
            # DQN
            for i in range(len(action_list)):
                if i + 1 not in legal_actions:
                    action_list[i] = float('-inf')
        return action_list, has_z, mega_elm

    def agent(self, state_shape, action_shape, model_type):
        learning_rate = 0.001
        init = tf.keras.initializers.HeUniform(seed=0)
        model = keras.Sequential()
        model.add(keras.layers.Dense(24, input_shape=state_shape, activation='relu', kernel_initializer=init))
        model.add(keras.layers.Dense(12, activation='relu', kernel_initializer=init))
        model.add(keras.layers.Dense(action_shape, activation='linear', kernel_initializer=init))
        model.compile(loss=tf.keras.losses.Huber(), optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
                      metrics=['accuracy'])
        sorted_files = glob.glob(''.join([MODEL_CKPT_PATH, model_type, '*.ckpt'])).sort(key=by_num)
        if sorted_files:
            model.load_weights(sorted_files[-1])
            num = findall(r'\d+', sorted_files[-1])[0]
            if model_type == MAIN_MODEL:
                self.main_ckpt_num = num
            else:
                self.tgt_ckpt_num = num
        return model

    def get_observation(self):
        """
        Order:
         - Active Poke DONE 0-18
            - Name
            - Ability
            - Item
            - Stats (x6)
            - Moves (x8)
            - Status
                - Base
                - Confuse
         - Field Settings DONE 19-25
            - Spikes
            - Stones
            - Toxic Spikes
            - Sticky Web
            - Light Screen
            - Reflect
            - Substitute
         - Player Team (x5) DONE 26-95
            - Name
            - Ability
            - Item
            - Stats (x6)
            - Moves (x4)
            - Status
         - Opp Active Poke DONE 96-110
            - Name
            - Ability
            - Item
            - Stats (x6)
            - Moves (x4)
            - Status
                - Base
                - Confuse
         - Field Settings DONE 111-117
            - Spikes
            - Stones
            - Toxic Spikes
            - Sticky Web
            - Light Screen
            - Reflect
            - Substitute
         - Opp Team (x5) 118-187
            - Name DONE
            - Ability
            - Item
            - Stats (x6)
            - Moves (x4) DONE
            - Status
         - Weather DONE 188-190
            - Weather
            - Terrain
            - Trick Room
        """
        # Base observation
        observation = np.array([-1] * self.state_shape[0])

        # Info lists
        move_list = list(self.battle_logger.move_map.keys())
        poke_list = list(self.battle_logger.stats_map.keys())
        move_list.sort(), poke_list.sort()

        print("observing player active")
        # Active Pokemon
        active_name = self.get_self_name()
        observation[0] = poke_list.index(active_name)

        ability, item = self.get_ability_item(self.Driver.SELF_SIDE)
        if '(base:' in ability:
            ability = ability.split('(')[0].strip()
        observation[1] = self.battle_logger.abilities_list.index(ability)
        if item != '' and 'None' not in item:
            if match(util.ITEM_TRICKED, item):
                item = search(util.ITEM_TRICKED, item).group(1)
            observation[2] = self.battle_logger.item_list.index(item)
        stats = self.get_stats(max_hp=False, do_ac=False)
        for i, s in enumerate(util.STATS_LIST):
            observation[i + 3] = stats[s]

        print("observing player moves")
        # Get self "move value"
        if not self.active_fainted():
            avail_moves, _, _ = self.move_options(modded=True)
            for v, m in avail_moves:
                if 'z' not in v:
                    index = int(v) + 8
                else:
                    index = int(v.replace('z', '')) + 12
                observation[index] = move_list.index(m.name)

        print("observing player statuses")
        for s in self.get_statuses(self.Driver.SELF_SIDE):
            text = s.text
            if text in util.STATUS_LIST:
                observation[17] = util.STATUS_LIST.index(text)
            if text == util.CONFUSED:
                observation[18] = 0

        print("observing player field")
        player_field = self.Driver.get_field_settings(self)
        for i, f in enumerate(util.FIELD_LIST):
            observation[19 + i] = player_field[f]

        print("observing player team")
        # Player Team
        set_index = 0
        for p in self.battle_logger.self_team:
            if p.name != active_name:
                observation[26 + (set_index * 14)] = poke_list.index(p.name)
                for j, m in enumerate(p.moves):
                    observation[35 + j + (set_index * 14)] = move_list.index(m)
                set_index += 1
        for i in range(1, 6):
            stats, status = self.get_stats(num=i, max_hp=False, get_status=True)
            ability, item = self.get_ability_item(self.Driver.SELF_SIDE, num=i, do_ac=False)
            if '(base:' in ability:
                ability = ability.split('(')[0].strip()
            observation[27 + (14 * (i - 1))] = self.battle_logger.abilities_list.index(ability)
            if item != '' and 'None' not in item:
                if match(util.ITEM_TRICKED, item):
                    item = search(util.ITEM_TRICKED, item).group(1)
                observation[28 + (14 * (i - 1))] = self.battle_logger.item_list.index(item)
            for j, s in enumerate(util.STATS_LIST):
                observation[29 + j + (14 * (i - 1))] = stats[s]
            if status != '':
                observation[39 + (14 * (i - 1))] = util.STATUS_LIST.index(status)

        print("observing opp active")
        # Opponent Active Pokemon
        opp_party = self.get_opp_party_status()
        opp_active = ''
        if any('active' in e.get_attribute('aria-label') for e in opp_party):
            opp_active = self.get_opp_name()
            observation[96] = poke_list.index(opp_active)
            abilities, item = self.get_ability_item(self.Driver.OPP_SIDE)
            if len(abilities) == 1:
                opp_ability = abilities[0]
                if '(base:' in opp_ability:
                    opp_ability = opp_ability.split('(')[0].strip()
                observation[97] = self.battle_logger.abilities_list.index(opp_ability)
            if item != '' and 'None' not in item:
                if match(util.ITEM_FRISKED, item):
                    item = search(util.ITEM_FRISKED, item).group(1)
                if match(util.ITEM_TRICKED, item):
                    item = search(util.ITEM_TRICKED, item).group(1)
                observation[98] = self.battle_logger.item_list.index(item)
            opp_stats = self.update_stats(self.battle_logger.stats_map.get(self.get_opp_name(), ["1.0"] * 5),
                                          hp_mod=self.get_opp_hp())
            for i in range(len(util.STATS_LIST)):
                observation[99 + i] = opp_stats[i]
            for i, m in enumerate(self.move_options(num=-1, do_ac=False)):
                observation[105 + i] = move_list.index(m)
            for s in self.get_statuses(self.Driver.OPP_SIDE):
                text = s.text
                if text in util.STATUS_LIST:
                    observation[109] = util.STATUS_LIST.index(text)
                if text == util.CONFUSED:
                    observation[110] = 0
        else:
            if any('fainted' in (label := e.get_attribute('aria-label')) for e in opp_party):
                opp_active = label.split("(")[0].strip()
        print("observing opp field")
        # Field Settings
        opp_field = self.Driver.get_field_settings(self.Driver.OPP_SIDE)
        for i, f in enumerate(util.FIELD_LIST):
            observation[111 + i] = opp_field[f]

        print("observing opp team")
        # Opp Team
        set_index = 0
        for i, p in enumerate(opp_party):
            label = p.get_attribute('aria-label')
            if opp_active != '' and opp_active not in label:
                name = label.split("(")[0].strip()
                observation[118 + (14 * set_index)] = poke_list.index(name)
                opp_team_abilities, opp_team_item = self.get_ability_item(self.Driver.OPP_SIDE, sidebar=True, elem=p)
                if len(opp_team_abilities) == 1:
                    opp_team_ability = opp_team_abilities[0]
                    if '(base:' in opp_team_ability:
                        opp_team_ability = opp_team_ability.split('(')[0].strip()
                    observation[119 + (14 * set_index)] = self.battle_logger.abilities_list.index(opp_team_ability)
                if opp_team_item != '' and 'None' not in opp_team_item:
                    if match(util.ITEM_FRISKED, opp_team_item):
                        opp_team_item = search(util.ITEM_FRISKED, opp_team_item).group(1)
                    if match(util.ITEM_TRICKED, opp_team_item):
                        opp_team_item = search(util.ITEM_TRICKED, opp_team_item).group(1)
                    observation[98] = self.battle_logger.item_list.index(opp_team_item)
                hp = 100.0
                if 'fainted' in label:
                    hp = 0.0
                elif '(' in label:
                    hp = float(findall(r'\d+.?\d+', label)[0])
                opp_status = []
                if '|' in label:
                    opp_status.append(search(r'\|([a-z]+)\)', label).group(1).upper())
                opp_team_stats = self.update_stats(self.battle_logger.stats_map.get(self.get_opp_name(), ["1.0"] * 5),
                                                   hp_mod=hp, stat_changes=opp_status)
                for j, s in enumerate(util.STATS_LIST):
                    observation[121 + j + (14 * (i - 1))] = opp_team_stats[s]
                poke = self.battle_logger.opp_team[i]
                for j, m in enumerate(poke.moves):
                    observation[127 + j + (14 * set_index)] = move_list.index(m)
                if opp_status:
                    observation[131 + (14 * set_index)] = util.STATUS_LIST.index(opp_status[0])
                set_index += 1

        print("observing weather")
        # Weather
        for w in self.get_weather():
            if w in util.WEATHER_LIST:
                observation[188] = util.WEATHER_LIST.index(w)
            if w in util.TERRAIN_LIST:
                observation[189] = util.TERRAIN_LIST.index(w)
            if w == util.W_TRICK_ROOM:
                observation[190] = 0
        return observation

    def calculate_reward(self, new_observation):
        poke_list = list(self.battle_logger.stats_map.keys())
        poke_list.sort()
        old_observation = self.observation
        player_party = [old_observation[0]]
        opp_party = [old_observation[96]]
        for i in range(5):
            player_party.append(old_observation[26 + (14 * i)])
            opp_party.append(old_observation[118 + (14 * i)])

        phc, ohc = 0.0, 0.0
        psc, osc = 0.0, 0.0
        ps, os = 0.0, 0.0
        pa, oa = 6, 6
        for p in player_party:
            if p == new_observation[0]:
                for j in range(6):
                    stat = self.battle_logger.stats_map[poke_list[p]][j]
                    c = ((new_observation[3 + j] / stat) - (old_observation[3 + j] / stat)) * 10
                    if j == 0:
                        if new_observation[3] == 0.0:
                            pa -= 1
                        phc += c
                    else:
                        psc += c
                ps += calc_status_change(old_observation[17], new_observation[17])
                ps += calc_status_change(old_observation[18], new_observation[18])
                continue
            for i in range(5):
                if p == new_observation[26 + (14 * i)]:
                    for j in range(6):
                        stat = self.battle_logger.stats_map[poke_list[p]][j]
                        index = 29 + j + (14 * i)
                        c = ((new_observation[index] / stat) - (old_observation[index] / stat)) * 10
                        if j == 0:
                            if new_observation[index] == 0.0:
                                pa -= 1
                            phc += c
                        else:
                            psc += c
                    ps += calc_status_change(old_observation[39 + (14 * i)], new_observation[39 + (14 * i)])
                    break

        for p in opp_party:
            if p == -1:
                continue
            if p == new_observation[96]:
                for j in range(6):
                    stat = self.battle_logger.stats_map[poke_list[p]][j]
                    c = ((old_observation[99 + j] / stat) - (new_observation[99 + j] / stat)) * 10
                    if j == 0:
                        if new_observation[99] == 0.0:
                            oa -= 1
                        ohc += c
                    else:
                        osc += c
                continue
            for i in range(5):
                if p == new_observation[118 + (14 * i)]:
                    for j in range(6):
                        stat = self.battle_logger.stats_map[poke_list[p]][j]
                        index = 121 + j + (14 * i)
                        c = ((old_observation[index] / stat) - (new_observation[index] / stat)) * 10
                        if j == 0:
                            if new_observation[index] == 0.0:
                                oa -= 1
                            ohc += c
                        else:
                            osc += c
                    os += calc_status_change(new_observation[132 + (14 * i)], old_observation[132 + (14 * i)])
                    break
        return phc - ohc + psc - osc + ps - os + (pa * 10) - (oa * 10)

    def __repr__(self):
        return 'NeuralNetBot'
