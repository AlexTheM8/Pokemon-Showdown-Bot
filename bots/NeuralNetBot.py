import os
import random
from re import findall, search, match

import numpy as np
import tensorflow as tf
from selenium.common import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from tensorflow import keras

from collections import deque
from bots.BattleBot import BattleBot
from util import util

MODEL_CKPT_PATH = './data/models/'
CKPT_FILE = 'checkpoint.ckpt'
checkpoint_path = ''.join([MODEL_CKPT_PATH, CKPT_FILE])
EPSILON_FILE = 'epsilon.data'
REPLAY_FILE = 'replay.data'


def train(replay_memory, model, target_model):
    learning_rate = 0.7
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

    X, Y = [], []
    for index, (observation, action, reward, new_observation, done) in enumerate(mini_batch):
        if not done:
            max_future_q = reward + discount_factor * np.max(future_qs_list[index])
        else:
            max_future_q = reward
        current_qs = current_qs_list[index]
        current_qs[action - 1] = (1 - learning_rate) * current_qs[action - 1] + learning_rate * max_future_q
        X.append(observation), Y.append(current_qs)
    model.fit(np.array(X), np.array(Y), batch_size=batch_size, verbose=0, shuffle=True)


def by_num(name):
    base, _ = name.split('.')
    _, num = base.split('_')
    return int(num)


def index_default(li, v, default=-1):
    try:
        return li.index(v)
    except ValueError:
        print("ERROR: '{}' is not in list".format(v))
        return default


def agent(state_shape, action_shape):
    learning_rate = 0.001
    init = tf.keras.initializers.HeUniform(seed=0)
    model = keras.Sequential()
    model.add(keras.layers.Dense(24, input_shape=state_shape, activation='relu', kernel_initializer=init))
    model.add(keras.layers.Dense(12, activation='relu', kernel_initializer=init))
    model.add(keras.layers.Dense(action_shape, activation='linear', kernel_initializer=init))
    model.compile(loss=tf.keras.losses.Huber(), optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
                  metrics=['accuracy'])
    return model


def save_training_info(epsilon, episode, replay_memory):
    with open(MODEL_CKPT_PATH + EPSILON_FILE, 'w', encoding='cp1252') as f:
        f.write(','.join([str(epsilon), str(episode)]))
    with open(MODEL_CKPT_PATH + REPLAY_FILE, 'w', encoding='cp1252') as f:
        lines = '\n'.join([
            '|'.join([repr(var).replace('\n', '').replace(' ', '').replace('array(', '').replace(')', '') for var in mem
                      ]) for mem in replay_memory])
        f.write(lines)


def load_training_info():
    with open(MODEL_CKPT_PATH + EPSILON_FILE, encoding='cp1252') as f:
        epsilon, episode = f.readline().split(',')
    replay_memory = deque(maxlen=50_000)
    with open(MODEL_CKPT_PATH + REPLAY_FILE, encoding='cp1252') as f:
        for line in f:
            observation, action, reward, new_observation, done = line.split('|')
            observation = np.array(eval(observation))
            new_observation = np.array(eval(new_observation))
            replay_memory.append([observation, int(action), float(reward), new_observation, bool(done)])
    return float(epsilon), int(episode), replay_memory


class NeuralNetBot(BattleBot):

    def __init__(self, headless):
        super().__init__(headless)
        self.epsilon, self.max_epsilon = 1, 1
        self.min_epsilon = 0.01
        self.decay = 0.001
        self.episode = 0

        self.state_shape, self.action_shape = (195,), 13
        self.model = agent(self.state_shape, self.action_shape)
        self.replay_memory = deque(maxlen=50_000)
        checkpoint_dir = os.path.dirname(checkpoint_path)
        latest = tf.train.latest_checkpoint(checkpoint_dir)
        if latest is None:
            self.model.save_weights(checkpoint_path)
            save_training_info(self.epsilon, self.episode, self.replay_memory)
        else:
            self.model.load_weights(latest)
            self.epsilon, self.episode, self.replay_memory = load_training_info()
        self.tgt_model = agent(self.state_shape, self.action_shape)
        self.tgt_model.set_weights(self.model.get_weights())

        self.target_update_counter = 0

        self.steps_to_update_target_model = 0
        self.observation = np.array([-1] * self.state_shape[0])
        self.total_training_rewards = 0

    def battle(self):
        super().battle()
        train(self.replay_memory, self.model, self.tgt_model)
        self.total_training_rewards += 1
        print('total reward:', self.total_training_rewards)
        self.model.save_weights(checkpoint_path)
        if self.steps_to_update_target_model >= 100:
            self.tgt_model.set_weights(self.model.get_weights())
            self.steps_to_update_target_model = 0
        self.epsilon = self.min_epsilon + (self.max_epsilon - self.min_epsilon) * np.exp(-self.decay * self.episode)
        self.episode += 1
        save_training_info(self.epsilon, self.episode, self.replay_memory)
        self.observation = np.array([-1] * self.state_shape[0])

    def battle_actions(self):
        try:
            if self.Driver.driver.find_elements(value="//div[contains(@class, 'statbar lstatbar')]/strong",
                                                by=By.XPATH):
                self.read_team(self.Driver.OPP_SIDE)
            # Check if used switching move
            if not self.Driver.driver.find_elements(value="//div[@class='movemenu']", by=By.XPATH):
                self.choose_action()
                return
            self.battle_logger.log_turn(self.Driver)
            if self.battle_logger.turn == 0:
                self.observation = self.get_observation()
            self.choose_action()
            self.battle_logger.turn += 1
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException) as e:
            print(e)
            return

    def choose_action(self):
        self.steps_to_update_target_model += 1
        if np.random.rand() <= self.epsilon:
            action_list, has_z, mega_elm = self.limit_actions()
            if action_list:
                action = random.choice(action_list)
            else:
                action = 1
        else:
            encoded = self.observation
            encoded_reshaped = encoded.reshape([1, encoded.shape[0]])
            predicted = self.model.predict(encoded_reshaped).flatten()
            action_list, has_z, mega_elm = self.limit_actions(predicted)
            action = np.argmax(action_list) + 1
        new_observation, reward, done = self.do_action(action, has_z, mega_elm)
        self.replay_memory.append([self.observation, action, reward, new_observation, done])

        self.observation = new_observation
        self.total_training_rewards += reward

    def do_action(self, action, has_z, mega_elm):
        if action <= 8:
            if action <= 4:
                if not has_z and mega_elm:
                    mega_elm[0].click()
                self.choose_move(str(action), has_z, mega_elm)
            else:
                self.choose_move('z' + str(action - 4), has_z, mega_elm)
        else:
            self.choose_switch(num=str(action - 8))
        done = self.Driver.wait_for_next_turn()
        new_observation = self.observation if done else self.get_observation()
        if done:
            reward = 300 if self.battle_logger.battle_win(self.Driver) else -300
        else:
            reward = self.calculate_reward(new_observation)
        print('action reward:', reward)
        return new_observation, reward, done

    def limit_actions(self, action_list=None):
        legal_actions = []
        has_z, mega_elm = False, None
        count = 0
        while len(legal_actions) == 0 and self.Driver.in_battle():
            options, has_z, mega_elm = self.move_options(do_mega=False)
            if has_z:
                moves, z_moves = [], []
                for v, _ in options:
                    if 'z' in v:
                        translation = int(v.replace('z', '')) + 4
                        z_moves.append(translation)
                    else:
                        moves.append(int(v))
                legal_actions = moves + z_moves
            else:
                legal_actions = [int(v) for v, _ in options]
            legal_actions = legal_actions + [int(p) + 8 for p in self.party_options()]
            if len(legal_actions) == 0:
                count += 1
                print('ERROR: Legal actions empty, trying again. Attempts:', count)
        if action_list is None:
            # Random
            action_list = legal_actions
        else:
            # DQN
            for i in range(len(action_list)):
                if i + 1 not in legal_actions:
                    action_list[i] = float('-inf')
        return action_list, has_z, mega_elm

    def get_observation(self):
        """
         - Active Poke: Name, Ability, Item, Stats (x6), Moves (x8), Status (x2) 0-18
         - Field Settings 19-26
         - Player Team (x5): Name, Ability, Item, Stats (x6), Moves (x4), Status 27-96
         - Opp Active Poke: Name, Ability, Item, Stats (x6), Moves (x4), Status (x2) 97-111
         - Field Settings 112-119
         - Opp Team (x5): Name, Ability, Item, Stats (x6), Moves (x4), Status 120-189
         - Weather 190-194
        """
        # Base observation
        observation = np.array([-1] * self.state_shape[0])

        # Info lists
        move_list = list(self.battle_logger.move_map.keys())
        poke_list = list(self.battle_logger.stats_map.keys())
        move_list.sort(), poke_list.sort()

        # Old info
        old_observation = self.observation
        player_party = [(old_observation[0], 0)]
        opp_party_ref = [(old_observation[96], 96)]
        for i in range(5):
            player_party.append((old_observation[27 + (14 * i)], 27 + (14 * i)))
            opp_party_ref.append((old_observation[120 + (14 * i)], 120 + (14 * i)))

        # Active Pokemon
        active_name = self.get_self_name()
        observation[0] = index_default(poke_list, active_name)
        ability, item = self.get_ability_item(self.Driver.SELF_SIDE)
        if '(base:' in ability:
            ability = ability.split('(')[0].strip()
        observation[1] = index_default(self.battle_logger.abilities_list, ability)
        if item != '' and 'None' not in item:
            if match(util.ITEM_GENERAL, item):
                item = search(util.ITEM_GENERAL, item).group(1)
            observation[2] = index_default(self.battle_logger.item_list, item)
        fainted = self.active_fainted()
        player_statuses = []
        if not fainted:
            player_statuses = self.get_statuses(self.Driver.SELF_SIDE)
        try:
            stats = self.get_stats(max_hp=False, do_ac=not fainted)
            for i, s in enumerate(util.STATS_LIST):
                observation[i + 3] = float(stats[s])
        except KeyError:
            # Ditto Case
            if not fainted:
                self.Driver.wait_for_element("//div[contains(@class, 'statbar rstatbar')]/strong", by=By.XPATH)
                elem_txt = self.Driver.driver.find_element(
                    value="//div[contains(@class, 'statbar rstatbar')]/div[@class='hpbar']/div[@class='hptext']",
                    by=By.XPATH).text.replace('%', '')
                hp = float(elem_txt) if elem_txt != '' else 100.0
            else:
                hp = 0.0
            stats = self.update_stats(self.battle_logger.stats_map[active_name], hp_mod=hp,
                                      stat_changes=player_statuses, provided=False)
            for i in range(len(util.STATS_LIST)):
                observation[i + 3] = float(stats[i])

        # Get self "move value"
        if not self.active_fainted():
            avail_moves, _, _ = self.move_options(modded=True, do_mega=False)
            for v, m in avail_moves:
                if 'z' not in v:
                    index = int(v) + 8
                else:
                    index = int(v.replace('z', '')) + 12
                observation[index] = index_default(move_list, m.name)

        if any((text := s.text) in util.STATUS_LIST for s in player_statuses):
            observation[17] = index_default(util.STATUS_LIST, text)
        if any(s.text == util.CONFUSED for s in player_statuses):
            observation[18] = 0

        # Opponent Active Pokemon
        opp_party = self.get_opp_party_status()
        opp_active = ''
        if any('active' in e.get_attribute('aria-label') for e in opp_party):
            opp_active = self.get_opp_name()
            observation[97] = index_default(poke_list, opp_active)
            abilities, item = self.get_ability_item(self.Driver.OPP_SIDE)
            if len(abilities) == 1:
                opp_ability = abilities[0]
                if '(base:' in opp_ability:
                    opp_ability = opp_ability.split('(')[0].strip()
                observation[98] = index_default(self.battle_logger.abilities_list, opp_ability)
            if item != '' and 'None' not in item:
                if match(util.ITEM_GENERAL, item):
                    item = search(util.ITEM_GENERAL, item).group(1)
                observation[99] = index_default(self.battle_logger.item_list, item)
            opp_statuses = self.get_statuses(self.Driver.OPP_SIDE)
            opp_stats = self.update_stats(self.battle_logger.stats_map.get(opp_active, ["1.0"] * 6),
                                          hp_mod=self.get_opp_hp(), stat_changes=opp_statuses, provided=False)
            opp_moves = self.move_options(num=-1, do_ac=False)
            for i in range(len(util.STATS_LIST)):
                observation[100 + i] = float(opp_stats[i])
                if i < len(opp_moves):
                    observation[106 + i] = index_default(move_list, opp_moves[i])
            if any((text := s.text) in util.STATUS_LIST for s in opp_statuses):
                observation[110] = index_default(util.STATUS_LIST, text)
            if any(s.text == util.CONFUSED for s in opp_statuses):
                observation[111] = 0
        else:
            if any('fainted' in (label := e.get_attribute('aria-label')) for e in opp_party):
                opp_active = label.split("(")[0].strip()

        player_party_side = self.get_self_party_status()
        set_index = 0
        for i in range(1, 7):
            if i < 6:
                # Player Team
                if str(i) in self.party_options():
                    path = self.Driver.CHOOSE_SWITCH_PATH
                    faint = False
                else:
                    path = self.Driver.FAINTED_SWITCH_PATH
                    faint = True
                n = self.Driver.driver.find_element(value=path.format(i), by=By.XPATH).text
                observation[27 + (14 * (i - 1))] = index_default(poke_list, n)
                skip = False
                if any((team_p := p)[0] == index_default(poke_list, n, -2) for p in player_party):
                    skip = old_observation[team_p[1] + 3] == 0.0
                if skip:
                    observation[30 + (14 * (i - 1))] = 0.0
                else:
                    exist_in_sidebar = any(n in (l := t.get_attribute('aria-label')) for t in player_party_side)
                    # Check if correct poke name from earlier and sidebar contains poke
                    if team_p[1] != 0 and team_p[0] == index_default(poke_list, n, -2) and exist_in_sidebar:
                        # Get old info
                        observation[28 + (14 * (i - 1))] = old_observation[team_p[1] + 1]
                        observation[29 + (14 * (i - 1))] = old_observation[team_p[1] + 2]
                        hp = 100.0
                        if 'fainted' in l:
                            hp = 0.0
                        elif search(r'\d+.?\d+', l):
                            hp = float(findall(r'\d+.?\d+', l)[0])
                        if '|' in l:
                            status = search(r'\|([a-z]+)\)', l).group(1).upper()
                            observation[40 + (14 * (i - 1))] = index_default(util.STATUS_LIST, status)
                        for j in range(len(util.STATS_LIST)):
                            if j == 0:
                                observation[30+(14*(i-1))] = (hp / 100.0) * float(self.battle_logger.stats_map[n][0])
                            else:
                                observation[30 + j + (14 * (i - 1))] = old_observation[team_p[1] + 3 + j]
                        if any((pk := player_p).name == n for player_p in self.battle_logger.self_team):
                            for j, m in enumerate(pk.moves):
                                observation[36 + j + (14 * (i - 1))] = index_default(move_list, m)
                    elif team_p[1] != 0 and team_p[0] == index_default(poke_list, n, -2) and not exist_in_sidebar:
                        observation[28 + (14 * (i - 1)):41 + (14 * (i - 1))] =\
                            old_observation[team_p[1] + 1:team_p[1] + 14]
                    else:
                        ability, item = self.get_ability_item(self.Driver.SELF_SIDE, num=i, do_ac=True)
                        if '(base:' in ability:
                            ability = ability.split('(')[0].strip()
                        observation[28 + (14 * (i - 1))] = index_default(self.battle_logger.abilities_list, ability)
                        if item != '' and 'None' not in item:
                            if match(util.ITEM_GENERAL, item):
                                item = search(util.ITEM_GENERAL, item).group(1)
                            observation[29 + (14 * (i - 1))] = index_default(self.battle_logger.item_list, item)
                        stats, status = self.get_stats(num=i, max_hp=False, get_status=True, fainted=faint, do_ac=False)
                        for j, s in enumerate(util.STATS_LIST):
                            observation[30 + j + (14 * (i - 1))] = float(stats[s])
                        if status != '':
                            observation[40 + (14 * (i - 1))] = index_default(util.STATUS_LIST, status)
                        if any((pk := player_p).name == n for player_p in self.battle_logger.self_team):
                            for j, m in enumerate(pk.moves):
                                observation[36 + j + (14 * (i - 1))] = index_default(move_list, m)

            # Opp Team
            if i - 1 < len(opp_party):
                p = opp_party[i - 1]
                label = p.get_attribute('aria-label')
                if opp_active != '' and opp_active not in label:
                    n = label.split("(")[0].strip()
                    observation[120 + (14 * set_index)] = index_default(poke_list, n)
                    skip = False
                    if any((opp_p := p)[0] == index_default(poke_list, n, -2) for p in opp_party_ref):
                        skip = old_observation[opp_p[1] + 3] == 0.0
                    if skip:
                        observation[123 + (14 * set_index)] = 0.0
                    else:
                        opp_team_abilities, opp_team_item = self.get_ability_item(self.Driver.OPP_SIDE, sidebar=True,
                                                                                  elem=p)
                        if len(opp_team_abilities) == 1:
                            opp_team_ability = opp_team_abilities[0]
                            if '(base:' in opp_team_ability:
                                opp_team_ability = opp_team_ability.split('(')[0].strip()
                            observation[121 + (14 * set_index)] = index_default(self.battle_logger.abilities_list,
                                                                                opp_team_ability)
                        if opp_team_item != '' and 'None' not in opp_team_item:
                            if match(util.ITEM_GENERAL, opp_team_item):
                                opp_team_item = search(util.ITEM_GENERAL, opp_team_item).group(1)
                            observation[122 + (14 * set_index)] = index_default(self.battle_logger.item_list,
                                                                                opp_team_item)
                        hp = 100.0
                        if 'fainted' in label:
                            hp = 0.0
                        elif search(r'\d+.?\d+', label):
                            hp = float(findall(r'\d+.?\d+', label)[0])
                        opp_status = []
                        if '|' in label:
                            opp_status.append(search(r'\|([a-z]+)\)', label).group(1).upper())
                        opp_team_stats = self.update_stats(self.battle_logger.stats_map.get(n, ["1.0"] * 6),
                                                           hp_mod=hp, stat_changes=opp_status)
                        for j in range(len(util.STATS_LIST)):
                            observation[123 + j + (14 * set_index)] = float(opp_team_stats[j])
                        if opp_status:
                            observation[133 + (14 * set_index)] = index_default(util.STATUS_LIST, opp_status[0])
                        if any((pk := opp_p).name == n for opp_p in self.battle_logger.opp_team):
                            for j, m in enumerate(pk.moves):
                                observation[129 + j + (14 * set_index)] = index_default(move_list, m)
                                if j == 3:
                                    break
                    set_index += 1

        # Field Settings
        player_field = self.Driver.get_field_settings(self.Driver.SELF_SIDE)
        opp_field = self.Driver.get_field_settings(self.Driver.OPP_SIDE)
        for i, f in enumerate(util.FIELD_LIST):
            observation[19 + i] = player_field[f]
            observation[112 + i] = opp_field[f]

        # Weather
        weather = self.get_weather()
        if any((wr := w) in util.WEATHER_LIST for w in weather):
            observation[190] = util.WEATHER_LIST.index(wr)
        if any((wr := w) in util.TERRAIN_LIST for w in weather):
            observation[191] = util.TERRAIN_LIST.index(wr)
        if util.W_TRICK_ROOM in weather:
            observation[192] = 0
        if util.W_TAILWIND in weather:
            observation[193] = 0
        if util.W_FOE_TAILWIND in weather:
            observation[194] = 0
        return observation

    def calculate_reward(self, new_observation):
        poke_list = list(self.battle_logger.stats_map.keys())
        poke_list.sort()
        old_observation = self.observation
        player_party = [(old_observation[0], 0)]
        opp_party = [(old_observation[97], 97)]
        opp_not_used = [(new_observation[97], 97)]
        for i in range(5):
            player_party.append((old_observation[27 + (14 * i)], 27 + (14 * i)))
            opp_party.append((old_observation[120 + (14 * i)], 120 + (14 * i)))
            opp_not_used.append((new_observation[120 + (14 * i)], 120 + (14 * i)))

        phc, ohc = 0.0, 0.0
        psc, osc = 0.0, 0.0
        ps, ost = 0.0, 0.0
        poa, ooa = self.battle_logger.player_alive, self.battle_logger.opp_alive
        pca, oca = 6, 6
        pf, of = 0.0, 0.0
        for i in range(6):
            # Player
            player_p, idx = player_party[i]
            if player_p == new_observation[0]:
                for j in range(6):
                    stat = float(self.battle_logger.stats_map[poke_list[player_p]][j])
                    c = ((new_observation[3 + j] / stat) - (old_observation[idx + 3 + j] / stat)) * 10
                    if j == 0:
                        if new_observation[3] == 0.0:
                            pca -= 1
                        phc += c
                    else:
                        psc += c
                if idx == 0:
                    ps += util.calc_status_change(old_observation[17], new_observation[17])
                    ps += util.calc_status_change(old_observation[18], new_observation[18])
                else:
                    ps += util.calc_status_change(old_observation[idx + 13], new_observation[17])
                    ps += util.calc_status_change(-1, new_observation[18])
            else:
                for j in range(5):
                    if player_p == new_observation[27 + (14 * j)]:
                        if old_observation[idx + 3] == 0.0:
                            pca -= 1
                        else:
                            for k in range(6):
                                stat = float(self.battle_logger.stats_map[poke_list[player_p]][k])
                                index = 30 + k + (14 * j)
                                c = ((new_observation[index] / stat) - (old_observation[idx + 3 + k] / stat)) * 10
                                if k == 0:
                                    if new_observation[index] == 0.0:
                                        pca -= 1
                                    phc += c * 2
                                else:
                                    psc += c
                            if idx == 0:
                                ps += util.calc_status_change(old_observation[17], new_observation[40 + (14 * j)])
                                ps += util.calc_status_change(old_observation[18], -1)
                            else:
                                ps += util.calc_status_change(old_observation[idx + 13], new_observation[40 + (14 * j)])
                            break

            # Opp
            opp_p, opp_i = opp_party[i]
            if opp_p == -1:
                continue
            if opp_p == new_observation[97]:
                opp_not_used.remove((new_observation[97], 97))
                if old_observation[opp_i + 3] == 0.0:
                    oca -= 1
                else:
                    f = False
                    for j in range(6):
                        stat = float(self.battle_logger.stats_map[poke_list[opp_p]][j])
                        c = ((old_observation[opp_i + 3 + j] / stat) - (new_observation[100 + j] / stat)) * 10
                        if j == 0:
                            ohc += c * 2
                            if new_observation[100] == 0.0:
                                oca -= 1
                                f = True
                                break
                        else:
                            osc += c
                    if not f:
                        if opp_i == 97:
                            ost += util.calc_status_change(new_observation[110], old_observation[110])
                            ost += util.calc_status_change(new_observation[111], old_observation[111])
                        else:
                            ost += util.calc_status_change(new_observation[110], old_observation[opp_i + 13])
                            ost += util.calc_status_change(new_observation[111], -1)
                    continue
            for j in range(5):
                if opp_p == new_observation[120 + (14 * j)]:
                    opp_not_used.remove((new_observation[120 + (14 * j)], 120 + (14 * j)))
                    if old_observation[opp_i + 3] == 0.0:
                        oca -= 1
                    else:
                        f = False
                        for k in range(6):
                            index = 123 + k + (14 * j)
                            stat = float(self.battle_logger.stats_map[poke_list[opp_p]][k])
                            c = ((old_observation[opp_i + 3 + k] / stat) - (new_observation[index] / stat)) * 10
                            if k == 0:
                                ohc += c * 2
                                if new_observation[index] == 0.0:
                                    oca -= 1
                                    f = True
                                    break
                            else:
                                osc += c
                        if not f:
                            if opp_i == 97:
                                ost += util.calc_status_change(new_observation[133 + (14 * j)], old_observation[110])
                                ost += util.calc_status_change(-1, old_observation[111])
                            else:
                                ost += util.calc_status_change(new_observation[133 + (14 * j)],
                                                               old_observation[opp_i + 13])
                        break
        for p, i in opp_not_used:
            if p == -1:
                continue
            f = False
            for j in range(6):
                stat = float(self.battle_logger.stats_map[poke_list[p]][j])
                c = (1.0 - (new_observation[i + 3 + j] / stat)) * 10
                if j == 0:
                    ohc += c * 2
                    if new_observation[i + 3] == 0.0:
                        oca -= 1
                        f = True
                        break
                else:
                    osc += c
            if not f:
                ost += util.calc_status_change(new_observation[i + 13], -1)
                if i + 14 == 111:
                    ost += util.calc_status_change(new_observation[111], -1)

        # Field changes
        for i in range(len(util.FIELD_LIST)):
            pf += util.calc_field_change(old_observation[19 + i], new_observation[19 + i], i)
            of += util.calc_field_change(new_observation[112 + i], old_observation[112 + i], i)

        pf += util.calc_field_change(old_observation[193], new_observation[193], 5)
        of += util.calc_field_change(new_observation[194], old_observation[194], 5)

        pa = pca - poa
        oa = ooa - oca
        self.battle_logger.player_alive = pca
        self.battle_logger.opp_alive = oca
        return phc + ohc + psc + osc + ps + ost + pf + of + (pa * 10) + (oa * 10)

    def __repr__(self):
        return 'NeuralNetBot'
