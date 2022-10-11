import glob
import random
from re import findall

import numpy as np
import tensorflow as tf
from selenium.common import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from tensorflow import keras

from collections import deque
from bots.BattleBot import BattleBot

'''
Sort data into winning & losing
Log init conditions & action taken
Bot will train on that data, then given init conditions & action, predict whether in win/lose
OR do reinforcement learning
Reward eq = PHC - OHC + PSC - OSC - PS + OS
P/OHC = Player/Opponent Health Change (100, -100)
P/OSC = Player/Opponent Stat Change (30, -30) 1 point per stat (max 6 per stat)
P/OS = Player/Opponent Status (10, -10) Whether gaining/losing a status condition
Equation range: (280, -280)
'''

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


class NeuralNetBot(BattleBot):

    def __init__(self):
        super().__init__()
        self.epsilon = 1
        self.max_epsilon = 1
        self.min_epsilon = 0.01
        self.decay = 0.001
        self.episode = 0
        self.main_ckpt_num, self.tgt_ckpt_num = 0, 0

        state_shape, action_shape = (108,), 13
        self.model = self.agent(state_shape, action_shape, MAIN_MODEL)
        self.tgt_model = self.agent(state_shape, action_shape, TGT_MODEL)
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
        reward = self.calculate_reward()
        return self.get_observation(), reward, False

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
            action_list[:] = [x for x in range(1, 14) if x in legal_actions]
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
        sorted_files = sorted(glob.glob(''.join([MODEL_CKPT_PATH, model_type, '*.ckpt'])))
        if len(sorted_files) > 0:
            model.load_weights(sorted_files[-1])
            num = findall(r'\d+', sorted_files[-1])[0]
            if model_type == MAIN_MODEL:
                self.main_ckpt_num = num
            else:
                self.tgt_ckpt_num = num
        return model

    def get_observation(self):
        # TODO Observation
        # TODO Save reward-calculating info
        return np.array([])

    def calculate_reward(self):
        # TODO Calculate Reward
        return 0

    def __repr__(self):
        return 'NeuralNetBot'
