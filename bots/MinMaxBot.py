import numpy as np

from collections import deque
from time import time

from selenium.common import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By

from bots.BattleBot import BattleBot


class Node:
    children = []

    def __init__(self, nid, parent_id, val=0, p_act=-1, opp_act=-1, cond_act=None):
        self.id = nid
        self.parent_id = parent_id
        self.value = val
        self.player_action, self.opp_action = p_act, opp_act
        if cond_act is None:
            self.conditions, self.player_actions, self.opp_actions = [], [], []
        else:
            self.conditions, self.player_actions, self.opp_actions = cond_act


class MinMaxBot(BattleBot):

    cond_val_table = {}

    def battle_actions(self):
        try:
            # TODO Check if necessary
            if self.Driver.driver.find_elements(value="//div[contains(@class, 'statbar lstatbar')]/strong",
                                                by=By.XPATH):
                self.read_team(self.Driver.OPP_SIDE)
            # Check if used switching move
            if not self.Driver.driver.find_elements(value="//div[@class='movemenu']", by=By.XPATH):
                self.choose_action()
                return
            self.battle_logger.log_turn(self.Driver)
            self.choose_action()
            self.battle_logger.turn += 1
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException) as e:
            print(e)
            return

    def choose_action(self):
        node = Node(0, -1, cond_act=self.get_cond_act())
        action = self.min_max(node, time())

    def min_max(self, root, run_time):
        node_list = [root]
        parent_index = 0
        action = root.player_action
        self.calc_node_value_and_children(root, node_list)
        queue = deque()
        queue.extend(root.children)
        node_list.extend(root.children)
        action_list = np.unique(np.array([n.player_action for n in root.children]))
        while queue and time() - run_time < 15:
            node = queue.pop()
            self.calc_node_value_and_children(node, node_list)
            node_list.extend(node.children)
            if not any(n.parent_id == parent_index for n in queue):
                # Completed searching specific children, update parent's value
                sub_parent = parent_index
                while sub_parent != 0:
                    parent_node = node_list[sub_parent]
                    parent_node.value = sum(c.value for c in parent_node.children) / len(parent_node.children)
                    sub_parent = parent_node.parent_id
                action_sum_count = [(0, 0)] * len(action_list)
                for c in node_list[0].children:
                    action_index = action_list.index(c.player_action)
                    old_sum, old_count = action_sum_count[action_index]
                    action_sum_count[action_index] = (old_sum + c.value, old_count + 1)
                best_action_index = np.argmax([v[0] / v[1] for v in action_sum_count])
                action = action_list[best_action_index]
                parent_index += 1
        queue.clear()
        return action

    def get_cond_act(self, prev_cond=None):
        # TODO Get Conditions: Player Team Stats & Moves, Opp Team Stats & Moves
        if prev_cond is None:
            # Base conditions
            pass
        else:
            # Calculated/assumed conditions
            pass
        return [], [], []

    def calc_node_value_and_children(self, node, node_list):
        if node.parent_id != -1:
            node.value = self.cond_val_table.get(node.conditions, self.calc_value(node))
            self.cond_val_table[node.conditions] = node.value
        for p_a in node.player_actions:
            for o_a in node.opp_actions:
                node.children.append(Node(len(node_list), node.id, p_act=p_a, opp_act=o_a,
                                          cond_act=self.get_cond_act(node.conditions)))

    def calc_value(self, node):
        # TODO Calc value
        return 0

    def __repr__(self):
        return 'MinMaxBot'
