from random import random
from re import match, search, findall

import numpy as np

from collections import deque
from time import time

from selenium.common import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By

from bots.BattleBot import BattleBot
from util.BattleLogger import Move
from util import util


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

    def get_cond_act(self, p_a=None, o_a=None, prev_cond=None):
        """
         - Active Poke: Name, Type (x2), Ability, Item, Stats (x6), Status (x2) 0-12
         - Player Team (x5): Name, Type (x2), Ability, Item, Stats (x6), Status 13-72
         - Opp Active Poke: Name, Type (x2), Ability, Item, Stats (x6), Status (x2) 73-85
         - Opp Team (x5): Name, Type (x2), Ability, Item, Stats (x6), Status 86-145
         - Field Settings 146-161
         - Weather 162-166
        """
        player_actions, opp_actions = [], []
        cond = [''] * 166
        if prev_cond is None:
            # TODO Get conditions from parent? At least conditions that haven't changed
            # TODO Optimize loops & AC
            # Actions
            switch = []
            count = 0
            while len(player_actions) == 0 and self.Driver.in_battle():
                options, _, _ = self.move_options(modded=True, do_mega=False)
                player_actions = options
                player_actions.sort(key=lambda o: o[1].name)
                switch = self.party_options(get_names=True)
                switch.sort(key=lambda poke: poke[1])
                player_actions = player_actions + switch
                if len(player_actions) == 0:
                    count += 1
                    print('ERROR: Legal actions empty, trying again. Attempts:', count)
            opp_party = self.get_opp_party_status()
            opp_active = ''
            if any('active' in e.get_attribute('aria-label') for e in opp_party):
                opp_active = self.get_opp_name()
                opp_actions = self.move_options(num=-1)
                opp_party.remove(opp_active)
                opp_actions.sort()
            opp_switch = []
            for e in opp_party:
                if 'fainted' not in (label := e.get_attribute('aria-label')):
                    opp_switch.append((label.split("(")[0].strip(), label, e))
            opp_switch.sort(key=lambda l: l[0])
            opp_actions = opp_actions + opp_party
            # Conditions
            # Player Active
            active_name = self.get_self_name()
            cond[0] = active_name
            for i, t in enumerate(self.Driver.get_type(self.Driver.SELF_SIDE)):
                cond[i + 1] = t
            ability, item = self.get_ability_item(self.Driver.SELF_SIDE)
            if '(base:' in ability:
                ability = ability.split('(')[0].strip()
            cond[3] = ability
            if item != '' and 'None' not in item:
                if match(util.ITEM_GENERAL, item):
                    item = search(util.ITEM_GENERAL, item).group(1)
                cond[4] = item
            fainted = self.active_fainted()
            player_statuses = self.get_statuses(self.Driver.SELF_SIDE)
            try:
                stats = self.get_stats(max_hp=False, do_ac=not fainted)
                for i, s in enumerate(util.STATS_LIST):
                    cond[i + 5] = stats[s]
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
                    cond[i + 5] = stats[i]
            for i, s in enumerate(player_statuses):
                cond[i + 11] = s

            # Player Party
            for i, p in enumerate(switch):
                cond[13 + (i * 12)] = p[1]
                poke_type = self.Driver.get_type(self.Driver.SELF_SIDE, int(p[0]))
                for j, t in enumerate(poke_type):
                    cond[14 + j + (i * 12)] = t
                poke_ability, p_item = self.get_ability_item(self.Driver.SELF_SIDE, num=p[0], do_ac=False)
                if '(base:' in poke_ability:
                    poke_ability = poke_ability.split('(')[0].strip()
                cond[16 + (i * 12)] = poke_ability
                if item != '' and 'None' not in item:
                    if match(util.ITEM_GENERAL, item):
                        item = search(util.ITEM_GENERAL, item).group(1)
                    cond[17 + (i * 12)] = p_item
                stats, status = self.get_stats(num=p[0], max_hp=False, get_status=True, do_ac=False)
                for j, s in enumerate(util.STATS_LIST):
                    cond[18 + j + (i * 12)] = stats[s]
                cond[24 + (i * 12)] = status

            # Opp Active
            if opp_active != '':
                cond[73] = opp_active
                opp_type = self.Driver.get_type(self.Driver.OPP_SIDE)
                for i, t in enumerate(opp_type):
                    cond[74 + i] = t
                ability, item = self.get_ability_item(self.Driver.OPP_SIDE, do_ac=False)
                if '(base:' in ability:
                    ability = ability.split('(')[0].strip()
                cond[76] = ability
                if item != '' and 'None' not in item:
                    if match(util.ITEM_GENERAL, item):
                        item = search(util.ITEM_GENERAL, item).group(1)
                    cond[77] = item
                opp_statuses = self.get_statuses(self.Driver.OPP_SIDE)
                opp_stats = self.update_stats(self.battle_logger.stats_map.get(opp_active, ["1.0"] * 6),
                                              hp_mod=self.get_opp_hp(), stat_changes=opp_statuses, provided=False)
                for i in range(len(util.STATS_LIST)):
                    cond[78 + i] = opp_stats[i]
                for i, s in opp_statuses:
                    cond[84 + i] = s
            # Opp Party
            for i, p in enumerate(opp_switch):
                cond[86 + (i * 12)] = p[0]
                opp_team_types = self.Driver.get_type(poke_elem=p[2])
                for j, t in enumerate(opp_team_types):
                    cond[87 + j + (i * 12)] = t
                opp_team_abilities, opp_team_item = self.get_ability_item(self.Driver.OPP_SIDE, sidebar=True, elem=p)
                if '(base:' in opp_team_abilities:
                    opp_team_abilities = opp_team_abilities.split('(')[0].strip()
                cond[89 + (i * 12)] = opp_team_abilities
                if opp_team_item != '' and 'None' not in opp_team_item:
                    if match(util.ITEM_GENERAL, opp_team_item):
                        opp_team_item = search(util.ITEM_GENERAL, opp_team_item).group(1)
                    cond[90 + (i * 12)] = opp_team_item
                hp = 100.0
                if search(r'\d+.?\d+', p[1]):
                    hp = float(findall(r'\d+.?\d+', p[1])[0])
                opp_status = []
                if '|' in p[1]:
                    opp_status.append(search(r'\|([a-z]+)\)', p[1]).group(1).upper())
                opp_team_stats = self.update_stats(self.battle_logger.stats_map.get(p[0], ["1.0"] * 6), hp_mod=hp,
                                                   stat_changes=opp_status)
                for j in range(len(util.STATS_LIST)):
                    cond[91 + j + (12 * i)] = opp_team_stats[j]
                if opp_status:
                    cond[97 + (12 * i)] = opp_status[0]
            # Field
            player_field = self.Driver.get_field_settings(self.Driver.SELF_SIDE)
            opp_field = self.Driver.get_field_settings(self.Driver.OPP_SIDE)
            for i, f in enumerate(util.FIELD_LIST):
                cond[146 + i] = player_field[f]
                cond[154 + i] = opp_field[f]
            # Weather
            weather = self.get_weather()
            if any((wr := w) in util.WEATHER_LIST for w in weather):
                cond[162] = wr
            if any((wr := w) in util.TERRAIN_LIST for w in weather):
                cond[163] = wr
            if util.W_TRICK_ROOM in weather:
                cond[164] = util.W_TRICK_ROOM
            if util.W_TAILWIND in weather:
                cond[165] = util.W_TAILWIND
            if util.W_FOE_TAILWIND in weather:
                cond[166] = util.W_FOE_TAILWIND
        else:
            # Calculated/assumed conditions
            # TODO Case of attack & switch move
            if self.player_goes_first(cond, p_a, o_a):
                if p_a[1] in self.battle_logger.stats_map:
                    # Switch
                    old_active_values = cond[:12]
                    new_active_values = [''] * 12
                    if any(cond[(index := 13 + (i * 12))] == p_a[1] for i in range(5)):
                        new_active_values = cond[index:index + 13]
                    cond[:12] = new_active_values
                    cond[12] = ''
                    cond[index:index + 13] = old_active_values
                else:
                    # Attack
                    p_stats = {}
                    for i, s in enumerate(cond[5:11]):
                        p_stats[util.STATS_LIST[i]] = float(s)
                    dmg = self.damage_calc(cond[1:3], p_a[1], cond[74:76], cond[76], cond[77], p_stats, cond[79:85])
                    opp_hp = max(0.0, float(cond[79]) - dmg)
                    cond[79] = str(opp_hp)
                    cond[1:13], cond[73:87] = self.effects_mod(p_a[1].effects, cond[1:13], cond[73:87], cond[146:])
                if o_a in self.battle_logger.stats_map:
                    # Switch
                    old_active_values = cond[73:86]
                    new_active_values = [''] * 12
                    if any(cond[(index := 86 + (i * 12))] == o_a for i in range(5)):
                        new_active_values = cond[index:index + 13]
                    cond[73:86] = new_active_values
                    cond[86] = ''
                    cond[index:index + 13] = old_active_values
                    # TODO Effects, switch field order and switch back
                else:
                    # Attack
                    o_stats = {}
                    data = self.battle_logger.move_map[o_a[1]]
                    o_move = self.battle_logger.move_map[data[0]] = Move(*data)
                    for i, s in enumerate(cond[79:85]):
                        o_stats[util.STATS_LIST[i]] = float(s)
                    dmg = self.damage_calc(cond[74:76], o_move, cond[1:3], cond[3], cond[4], o_stats, cond[5:11])
                    p_hp = max(0.0, float(cond[5]) - dmg)
                    cond[5] = str(p_hp)
                    # TODO Move effects
            else:
                if o_a in self.battle_logger.stats_map:
                    # Switch
                    pass
                else:
                    # Attack
                    pass
                if p_a[1] in self.battle_logger.stats_map:
                    # Switch
                    pass
                else:
                    # Attack
                    pass
            # TODO Post-turn actions (poison, leftovers, abilities, etc)
        return cond, player_actions, opp_actions

    def player_goes_first(self, conditions, p_a, o_a):
        # TODO Tailwind
        p_switch = p_a[1] in self.battle_logger.stats_map
        o_switch = o_a in self.battle_logger.stats_map
        # Switch & Pursuit
        if p_switch:
            if o_a == 'Pursuit':
                return False
            return True
        if o_switch:
            if p_a[1].name == 'Pursuit':
                return True
            return False
        o_move = self.battle_logger.move_map[o_a]
        # Priority
        if p_a[1].effects.priority > o_move.effects.priority:
            return True
        elif p_a[1].effects.priority < o_move.effects.priority:
            return False
        # Speed Check
        return conditions[10] >= conditions[89]

    def effects_mod(self, effects, user_info, target_info, field_info):
        # TODO Counter, Stats Steal, Stats Clear, Flinch, Crit, Switch
        for s in effects.stat_change:
            if s[3] and random() > 0.25:
                continue
            stat_index = 5 + util.STATS_LIST.index(s[0])
            if s[1] == util.USER:
                user_info[stat_index] += user_info[stat_index] * int(s[2]) * 0.268
            else:
                target_info[stat_index] += target_info[stat_index] * int(s[2]) * 0.268
        if effects.status is not None:
            if not effects.status[2] or random() <= 0.25:
                if effects.status[1] == util.USER:
                    # TODO Disabled, Encore, Infestation
                    if effects.status[0] == util.CONFUSED:
                        user_info[-1] = effects.status[0]
                    else:
                        user_info[-2] = effects.status[0]
                else:
                    if effects.status[0] == util.CONFUSED:
                        target_info[-1] = effects.status[0]
                    else:
                        target_info[-2] = effects.status[0]
        if effects.field is not None:
            if effects.field in util.FIELD_LIST[:4]:
                field_info[7 + util.FIELD_LIST.index(effects.field)] += 1
            else:
                field_info[util.FIELD_LIST.index(effects.field)] += 1
        if effects.weather is not None:
            field_info[16] = effects.weather
        return user_info, target_info

    def calc_node_value_and_children(self, node, node_list):
        if node.parent_id != -1:
            # TODO Comparison function
            node.value = self.cond_val_table.get(node.conditions, self.calc_value(node))
            self.cond_val_table[node.conditions] = node.value
        for p_a in node.player_actions:
            for o_a in node.opp_actions:
                node.children.append(Node(len(node_list), node.id, p_act=p_a, opp_act=o_a,
                                          cond_act=self.get_cond_act(p_a, o_a, node.conditions)))

    def calc_value(self, node):
        # TODO Calc value
        return 0

    def __repr__(self):
        return 'MinMaxBot'
