from copy import copy
from joblib import Parallel, delayed
from itertools import product
from multiprocessing import cpu_count
from random import random, choice
from re import match, search, findall

import numpy as np

from collections import deque
from time import time

from selenium.common import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By

from bots.BattleBot import BattleBot, set_stat_stages
from util import util

num_cores = cpu_count() - 1


class Node:

    def __init__(self, nid, parent_id, val=float('-inf'), p_act=-1, opp_act=-1, cond_act=None):
        self.id, self.parent_id = nid, parent_id
        self.value = val
        self.children = []
        self.player_action, self.opp_action = p_act, opp_act
        if cond_act is None:
            self.conditions, self.player_actions, self.opp_actions = [], [], []
        else:
            self.conditions, self.player_actions, self.opp_actions = cond_act

    def __repr__(self):
        return 'Node: ' + str(self.id)


def calc_stat_by_stage(base, stage):
    stage_dict = {
        1: 1.5,
        2: 2,
        3: 2.5,
        4: 3,
        5: 3.5,
        6: 4,
        -1: 2 / 3,
        -2: 0.5,
        -3: 2 / 5,
        -4: 1 / 3,
        -5: 2 / 7,
        -6: 0.25
    }
    return base + (base * stage_dict.get(stage, 1))


def can_move(statuses):
    odds = 1
    if statuses[0] == util.PAR or statuses[0] == util.FRZ or statuses[0] == util.SLP:
        odds *= 0.5
    if statuses[1] == util.CONFUSED:
        odds *= 0.5
    return random() <= odds


def status_can_effect(status, types, curr_status):
    if curr_status != '':
        return False
    if status == util.FRZ:
        return util.ICE not in types
    if status == util.PSN or status == util.TOX:
        return util.POISON not in types and util.STEEL not in types
    if status == util.PAR:
        return util.ELECTR not in types
    return True


def update_field(move, field_info, field_index):
    if move.effects.field == util.SCREEN_CLEAR:
        field_info[12:15] = [0] * 3
    elif move.effects.field == util.FIELD_CLEAR:
        field_info[:4] = [0] * 4
    elif move.effects.field == util.W_TRICK_ROOM:
        field_info[-3] = util.W_TRICK_ROOM
    elif move.effects.field == util.W_TAILWIND:
        field_info[-2] = util.W_TAILWIND
    elif move.effects.field == util.FIELD_SPIKES:
        count = min(3, field_info[field_index + util.FIELD_LIST.index(move.effects.field)] + 1)
        field_info[field_index + util.FIELD_LIST.index(move.effects.field)] = count
    elif move.effects.field == util.FIELD_POISON:
        count = min(2, field_info[field_index + util.FIELD_LIST.index(move.effects.field)] + 1)
        field_info[field_index + util.FIELD_LIST.index(move.effects.field)] = count
    elif move.effects.field == util.FIELD_WEB:
        field_info[field_index + util.FIELD_LIST.index(move.effects.field)] = 1
    elif move.effects.field == util.FIELD_STONES:
        field_info[field_index + util.FIELD_LIST.index(move.effects.field)] = 1
    elif move.effects.field in util.FIELD_LIST:
        field_info[util.FIELD_LIST.index(move.effects.field)] = 1
    return field_info


class MinMaxBot(BattleBot):
    cond_val_table = {}
    P_LOCK, O_LOCK = 0, 0
    P_PROTECT, O_PROTECT = 1.0, 1.0
    P_TOX, O_TOX = 0, 0
    P_STAT_STAGES, O_STAT_STAGES = [0] * 5, [0] * 5
    P_SUB_HP, O_SUB_HP = 0.0, 0.0
    COND_CHECK = [''] * 167

    # TODO Eval processing time & optimize

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
            self.choose_action()
            self.battle_logger.turn += 1
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException) as e:
            print(e)
            return

    def choose_action(self):
        t = time()
        node = Node(0, -1, cond_act=self.get_cond_act())
        action = self.min_max(node, t)
        print(action)
        if action[1] in self.battle_logger.stats_map:
            self.choose_switch(action[0])
        else:
            _, has_z, mega_elm = self.move_options(do_mega=False)
            if 'z' in action[0]:
                self.choose_move('z' + action[0], has_z, mega_elm)
            else:
                if not has_z and mega_elm:
                    mega_elm[0].click()
                self.choose_move(str(action[0]), has_z, mega_elm)
        self.Driver.wait_for_next_turn()

    def min_max(self, root, run_time):
        node_list = [root]
        parent_index = 0
        root = self.calc_node_value_and_children(root, node_list)
        node_list[0] = root
        queue = deque()
        queue.extend(root.children)
        node_list.extend(root.children)
        action_list = []
        for n in root.children:
            if n.player_action not in action_list:
                action_list.append(n.player_action)
        if len(action_list) == 1:
            return action_list[0]
        alt_action_list = []
        for a in action_list:
            if a[1] in self.battle_logger.stats_map:
                alt_action_list.append(a[1])
            else:
                alt_action_list.append(a[1].name)
        # TODO Select action, check if waiting on opp, if so, search more
        while queue and time() - run_time < 10:
            node = queue.popleft()
            print(node.id)
            node = self.calc_node_value_and_children(node, node_list)
            node_list[node.id] = node
            node_list.extend(node.children)
            queue.extend(node.children)
            if not any(n.parent_id == parent_index for n in queue):
                # Completed searching specific children, update parent's value
                sub_parent = parent_index
                while sub_parent != 0:
                    parent_node = node_list[sub_parent]
                    total, count = 0, -1
                    for c in parent_node.children:
                        if c.value != float('inf'):
                            total += c.value
                        if count == -1:
                            count = 0
                        count += 1
                    if total != 0:
                        parent_node.value += (total / count) * 0.1
                    sub_parent = parent_node.parent_id
        action_sum_count = [(0, -1)] * len(action_list)
        for c in root.children:
            if c.value == float('-inf'):
                continue
            # print(c.value)
            if c.player_action[1] in self.battle_logger.stats_map:
                action_index = alt_action_list.index(c.player_action[1])
            else:
                action_index = alt_action_list.index(c.player_action[1].name)
            old_sum, old_count = action_sum_count[action_index]
            if old_count == -1:
                old_count = 0
            action_sum_count[action_index] = (old_sum + c.value, old_count + 1)
        best_action_index = np.argmax([v[0] / v[1] for v in action_sum_count])
        action = action_list[best_action_index]
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
        player_party = [(self.COND_CHECK[0], 0)]
        opp_party_ref = [(self.COND_CHECK[73], 73)]
        for i in range(5):
            player_party.append((self.COND_CHECK[13 + (12 * i)], 13 + (12 * i)))
            opp_party_ref.append((self.COND_CHECK[86 + (12 * i)], 86 + (12 * i)))
        player_actions, opp_actions = [], []
        if not prev_cond:
            cond = [''] * 167
            self.P_LOCK, self.O_LOCK = 0, 0
            # Actions
            switch = []
            count = 0
            fainted = self.active_fainted()
            active_name = self.get_self_name()
            cond[0] = active_name
            while len(player_actions) == 0 and self.Driver.in_battle():
                if not fainted:
                    options, _, _ = self.move_options(modded=True, do_mega=False)
                    player_actions = options
                switch = self.get_switch(cond)
                player_actions = player_actions + switch
                if len(player_actions) == 0:
                    count += 1
                    print('ERROR: Legal actions empty, trying again. Attempts:', count)
            opp_party = self.get_opp_party_status()
            opp_active = ''
            opp_moves = []
            if any('active' in (elem := e).get_attribute('aria-label') for e in opp_party):
                opp_active = self.get_opp_name()
                opp_moves = [self.battle_logger.move_map[m] for m in self.move_options(num=-1)]
                opp_moves = self.rand_moves(opp_moves, opp_active)
                opp_party.remove(elem)
                # opp_moves.sort(key=lambda v: v.name)
            opp_switch = []
            for e in opp_party:
                if 'fainted' not in (label := e.get_attribute('aria-label')):
                    opp_switch.append((label.split("(")[0].strip(), label, e))
            # opp_switch.sort(key=lambda l: l[0])
            opp_actions = opp_moves + [n for n, _, _ in opp_switch]
            # Conditions
            # Player Active
            ability, item = self.get_ability_item(self.Driver.SELF_SIDE)
            self.P_TOX = self.get_tox_count()
            for i, t in enumerate(self.Driver.get_type(self.Driver.SELF_SIDE, do_ac=False)):
                cond[i + 1] = t
            if '(base:' in ability:
                ability = ability.split('(')[0].strip()
            cond[3] = ability
            if item != '' and 'None' not in item:
                if match(util.ITEM_GENERAL, item):
                    item = search(util.ITEM_GENERAL, item).group(1)
                cond[4] = item
            player_statuses = []
            if not fainted:
                player_statuses = self.get_statuses(self.Driver.SELF_SIDE)
                self.P_STAT_STAGES = set_stat_stages(player_statuses)
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
            if any((text := s.text) in util.STATUS_LIST for s in player_statuses):
                cond[11] = text
            if any(s.text == util.CONFUSED for s in player_statuses):
                cond[12] = util.CONFUSED

            # Player Party
            player_party_side = self.get_self_party_status()
            for i, p in enumerate(switch):
                team_p = None
                for m in player_party:
                    if m[0] == p[1]:
                        team_p = m
                        break
                exist_in_sidebar = any(p[1] in (l := t.get_attribute('aria-label')) for t in player_party_side)
                # Check if correct poke name from earlier and sidebar contains poke
                if exist_in_sidebar and team_p is not None and team_p[1] != 0:
                    # Get old info
                    cond[13 + (12 * i):18 + (12 * i)] = self.COND_CHECK[team_p[1]:team_p[1] + 5]
                    hp = 100.0
                    if 'fainted' in l:
                        hp = 0.0
                    elif search(r'\d+.?\d+', l):
                        hp = float(findall(r'\d+.?\d+', l)[0])
                    if '|' in l:
                        cond[24 + (12 * i)] = search(r'\|([a-z]+)\)', l).group(1).upper()
                    for j in range(len(util.STATS_LIST)):
                        if j == 0:
                            cond[18 + (12 * i)] = str((hp / 100.0) * float(self.battle_logger.stats_map[p[1]][0]))
                        else:
                            cond[18 + j + (12 * i)] = self.COND_CHECK[team_p[1] + 5 + j]
                elif team_p is not None and team_p[1] != 0 and not exist_in_sidebar:
                    cond[13 + (12 * i):25 + (12 * i)] = self.COND_CHECK[team_p[1]:team_p[1] + 12]
                else:
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
                # print('Opp Active:', opp_active)
                opp_type = self.Driver.get_type(self.Driver.OPP_SIDE)
                for i, t in enumerate(opp_type):
                    cond[74 + i] = t
                ability, item = self.get_ability_item(self.Driver.OPP_SIDE, do_ac=False)
                self.O_TOX = self.get_tox_count()
                if len(ability) == 1:
                    if '(base:' in ability[0]:
                        ability[0] = ability[0].split('(')[0].strip()
                    cond[76] = ability[0]
                if item != '' and 'None' not in item:
                    if match(util.ITEM_GENERAL, item):
                        item = search(util.ITEM_GENERAL, item).group(1)
                    cond[77] = item
                opp_statuses = self.get_statuses(self.Driver.OPP_SIDE)
                self.O_STAT_STAGES = set_stat_stages(opp_statuses)
                opp_stats = self.update_stats(self.battle_logger.stats_map.get(opp_active, ["1.0"] * 6),
                                              hp_mod=self.get_opp_hp(), stat_changes=opp_statuses, provided=False)
                cond[78:84] = opp_stats
                if any((text := s.text) in util.STATUS_LIST for s in opp_statuses):
                    cond[84] = text
                if any(s.text == util.CONFUSED for s in opp_statuses):
                    cond[85] = util.CONFUSED
            # Opp Party
            for i, p in enumerate(opp_switch):
                cond[86 + (i * 12)] = p[0]
                opp_team_types = self.Driver.get_type(None, poke_elem=p[2])
                for j, t in enumerate(opp_team_types):
                    cond[87 + j + (i * 12)] = t
                opp_team_abilities, opp_team_item = self.get_ability_item(self.Driver.OPP_SIDE, sidebar=True, elem=p[2])
                if len(ability) == 1:
                    if '(base:' in opp_team_abilities[0]:
                        opp_team_abilities[0] = opp_team_abilities[0].split('(')[0].strip()
                    cond[89 + (i * 12)] = opp_team_abilities[0]
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
            self.COND_CHECK = copy(cond)
            # print('First check:', cond)
        else:
            # TODO if used a z-move, remove from options & update item
            # Calculated/assumed conditions
            cond = copy(prev_cond)
            # print("Start calc:", cond)
            effects = ([False, False, False, False], ['', False, False, False, False, False, False], False)
            o_eff = ([False, False, False, False], ['', False, False, False, False, False, False], False)
            dmg, o_dmg = 0.0, 0.0
            if self.player_goes_first(cond, p_a, o_a):
                if p_a:
                    if p_a[1] in self.battle_logger.stats_map:
                        self.player_switch(cond, p_a)
                        # print('Post-switch:', cond)
                    else:
                        if cond[73] != '' and can_move(cond[11:13]):
                            effects = self.player_attack(cond, p_a)
                            if effects[0][0]:
                                return self.player_switch_move(cond)
                            # print('Post-attack:', cond)
                if cond[73] != '' and float(cond[78]) > 0.0:
                    if effects[1][4]:
                        self.opp_switch(cond, None)
                    elif o_a in self.battle_logger.stats_map:
                        self.opp_switch(cond, o_a)
                    elif not effects[1][1] and o_a:
                        # Attack
                        if can_move(cond[84:86]) and self.fp_check(o_a, p_a[1]):
                            _, o_moves = self.get_o_poke_and_moves(cond, o_a)
                            if (not self.protect(effects[1][2], self.Driver.SELF_SIDE)
                                or o_a.move_type == util.STATUS) and (not effects[1][5] or o_a.type != util.GROUND
                                                                      or o_a.move_type == util.STATUS):
                                # print('Before eff:', cond, o_a)
                                cond[74:86], cond[1:13], cond[146:], o_dmg, o_eff = \
                                    self.dmg_effects(self.Driver.OPP_SIDE, o_a, cond, o_moves)
                                # print('After eff:', cond, o_a)
                                if p_a[1] not in self.battle_logger.stats_map:
                                    if o_eff[1][0] == p_a[1].move_type:
                                        o_dmg = dmg * 2
                                if cond[53] == 1:
                                    self.P_SUB_HP = max(0.0, self.P_SUB_HP - dmg)
                                    if self.P_SUB_HP <= 0.0:
                                        cond[53] = 0
                                else:
                                    cond[5] = max(0.0, float(cond[5]) - o_dmg)
                                    if cond[4] == 'Sitrus Berry':
                                        poke = self.get_poke(cond)
                                        if 0.0 < float(cond[5]) <= float(poke.stats[util.HP]) * 0.5:
                                            cond[5] = float(cond[5]) + (float(poke.stats[util.HP]) * 0.25)
                                            cond[4] = ''
                                base_hp = float(self.battle_logger.stats_map[cond[73]][0])
                                if cond[77] == 'Life Orb' and o_dmg > 0.0:
                                    cond[78] = max(0.0, float(cond[78]) - base_hp * 0.1)
                                if effects[1][3] and o_a.move_type == util.PHYSICAL:
                                    cond[78] = max(0.0, float(cond[78]) - base_hp * 0.125)
                                if o_eff[1][4]:
                                    self.player_switch(cond, None)
                                if o_eff[0][0]:
                                    self.opp_switch(cond, None)
            else:
                if o_a in self.battle_logger.stats_map:
                    self.opp_switch(cond, o_a)
                else:
                    # Attack
                    if can_move(cond[84:86]) \
                            and (o_a.name != 'Sucker Punch' or (p_a and p_a[1] not in self.battle_logger.stats_map
                                                                and p_a[1].move_type != util.STATUS)):
                        o_poke, o_moves = self.get_o_poke_and_moves(cond, o_a)
                        cond[74:86], cond[1:13], cond[146:], o_dmg, o_eff = self.dmg_effects(self.Driver.OPP_SIDE,
                                                                                             o_a, cond, o_moves)
                        if cond[53] == 1:
                            self.P_SUB_HP = max(0.0, self.P_SUB_HP - dmg)
                            if self.P_SUB_HP <= 0.0:
                                cond[53] = 0
                        else:
                            cond[5] = max(0.0, float(cond[5]) - o_dmg)
                            if cond[4] == 'Sitrus Berry':
                                poke = self.get_poke(cond)
                                if 0.0 < float(cond[5]) <= float(poke.stats[util.HP]) * 0.5:
                                    cond[5] = float(cond[5]) + (float(poke.stats[util.HP]) * 0.25)
                                    cond[4] = ''
                        if cond[77] == 'Life Orb' and o_dmg > 0.0:
                            base_hp = float(self.battle_logger.stats_map[cond[73]][0])
                            cond[78] = max(0.0, float(cond[78]) - base_hp * 0.1)
                        if o_eff[0][1]:
                            self.opp_switch(cond, None)
                if float(cond[5]) > 0.0:
                    if o_eff[1][4]:
                        self.player_switch(cond, None)
                    elif p_a[1] in self.battle_logger.stats_map:
                        self.player_switch(cond, p_a)
                    elif not o_eff[1][1] and p_a:
                        # Attack
                        if (not self.protect(o_eff[1][2], self.Driver.OPP_SIDE)
                            or p_a[1].move_type == util.STATUS) \
                                and (not o_eff[1][5] or p_a[1].type != util.GROUND
                                     or p_a[1].move_type == util.STATUS) and self.fp_check(p_a[1], o_a):
                            effects = self.player_attack(cond, p_a, o_a, o_dmg)
                            if o_eff[1][3] and p_a[1].move_type == util.PHYSICAL:
                                base_hp = float(self.battle_logger.stats_map[cond[0]][0])
                                cond[5] = max(0.0, float(cond[5]) - base_hp * 0.125)
                            if cond[4] == 'Sitrus Berry':
                                poke = self.get_poke(cond)
                                if 0.0 < float(cond[5]) <= float(poke.stats[util.HP]) * 0.5:
                                    cond[5] = float(cond[5]) + (float(poke.stats[util.HP]) * 0.25)
                                    cond[4] = ''
                            if o_eff[1][4]:
                                self.opp_switch(cond, None)
                            if effects[0][0]:
                                return self.player_switch_move(cond)
            self.post_turn_effects(cond, 0)
            self.post_turn_effects(cond, 73)
            p_fainted, o_fainted = cond[0] == '' or float(cond[5]) <= 0.0, cond[73] == '' or float(cond[78]) <= 0.0
            if p_fainted:
                self.P_LOCK = 0
            elif effects[0][3] and self.P_LOCK == 0:
                self.P_LOCK = 3
            elif self.P_LOCK > 0:
                self.P_LOCK -= 1
            if o_fainted:
                self.O_LOCK = 0
            elif o_eff[0][3] and self.O_LOCK == 0:
                self.O_LOCK = 3
            elif self.O_LOCK > 0:
                self.O_LOCK -= 1
            if p_fainted:
                player_actions = self.get_switch(cond)
            elif effects[0][1]:
                player_actions = []
            elif effects[0][2] or self.P_LOCK > 0:
                player_actions = [p_a]
            else:
                poke = self.get_poke(cond)
                if p_a[1] not in self.battle_logger.stats_map and 'Choice' in cond[4]:
                    moves = [p_a]
                else:
                    moves = [('', self.battle_logger.move_map[m]) for m in poke.moves]
                player_actions = moves + self.get_switch(cond)
            if o_fainted:
                opp_actions = [p.name for p in self.get_opp_team_copy(cond)]
            elif o_eff[0][1]:
                opp_actions = []
            elif o_eff[0][2] or self.O_LOCK > 0:
                opp_actions = [o_a]
            else:
                if o_a and o_a not in self.battle_logger.stats_map and 'Choice' in cond[77]:
                    o_moves = [o_a]
                else:
                    _, o_moves = self.get_o_poke_and_moves(cond, o_a)
                opp_actions = o_moves + [p.name for p in self.get_opp_team_copy(cond)]
            # print('Calculated check:', cond)
        return cond, self.filter_p_act(player_actions, cond), self.filter_o_act(opp_actions, cond)

    def rand_moves(self, moves, poke):
        if len(moves) < 4:
            possible_moves = copy(self.battle_logger.known_move_map[poke])
            for m in moves:
                if m.name in possible_moves:
                    possible_moves.remove(m.name)
            for _ in range(4 - len(moves)):
                if possible_moves:
                    c = choice(possible_moves)
                    moves.append(self.battle_logger.move_map[c])
                    possible_moves.remove(c)
                else:
                    break
        return moves

    def get_tox_count(self):
        self.Driver.wait_for_element("//div[contains(@class, 'tooltip tooltip-')]", by=By.XPATH)
        if elem := self.Driver.driver.find_elements(value="//*[contains(text(), 'Next damage:')]", by=By.XPATH):
            return min(15.0, float(search(r'Next damage: (\d+.?\d+)%', elem.text).group(1)) // 6)
        return 0.0

    def player_goes_first(self, conditions, p_a, o_a):
        if not p_a:
            return False
        if not o_a:
            return True
        p_switch = p_a[1] in self.battle_logger.stats_map
        o_switch = o_a in self.battle_logger.stats_map
        # Switch & Pursuit
        if p_switch:
            if o_a == 'Pursuit':
                return False
            return True
        if o_switch:
            if not p_switch:
                if p_a[1].name == 'Pursuit':
                    return True
            return False
        # Priority
        if p_a[1].effects.priority > o_a.effects.priority:
            return True
        elif p_a[1].effects.priority < o_a.effects.priority:
            return False
        # Speed Check
        p_spd = float(conditions[10]) * 2 if conditions[165] else float(conditions[10])
        o_spd = float(conditions[83]) * 2 if conditions[166] else float(conditions[83])
        if conditions[164] != '':
            return p_spd >= o_spd
        else:
            return p_spd <= o_spd

    def protect(self, used, user):
        if not used:
            if user == self.Driver.SELF_SIDE:
                self.P_PROTECT = 1.0
            else:
                self.O_PROTECT = 1.0
            return False
        if user == self.Driver.SELF_SIDE:
            odds = random() <= self.P_PROTECT
            self.P_PROTECT /= 3.0
        else:
            odds = random() <= self.O_PROTECT
            self.O_PROTECT /= 3.0
        return odds

    def dmg_effects(self, side, move, cond, user_moves):
        player_p = self.get_poke(cond)
        player_stats = [player_p.stats[st] for st in util.STATS_LIST[1:]]
        if side == self.Driver.SELF_SIDE:
            user_info = cond[1:13]
            target_info = cond[74:86]
            field_info = cond[146:]
            user_base_hp = float(player_p.stats[util.HP])
            target_base_hp = float(self.battle_logger.stats_map[cond[73]][0])
            user_base = player_stats
            target_base = self.battle_logger.stats_map[cond[73]][1:]
        else:
            user_info = cond[74:86]
            target_info = cond[1:13]
            field_info = cond[154:162] + cond[146:154] + cond[162:165] + [cond[166], cond[165]]
            user_base_hp = float(self.battle_logger.stats_map[cond[73]][0])
            target_base_hp = float(player_p.stats[util.HP])
            user_base = self.battle_logger.stats_map[cond[73]][1:]
            target_base = player_stats
        # Format: Switch, Recharge, Charge, Move Lock
        user_effects = [False, False, False, False]
        # Format: Counter[str], Flinch, Protect, Contact dmg, Switch, Levitate, Move Lock
        target_effects = ['', False, False, False, False, False, False]
        # Format: Move Lock
        move_lock = False
        u_stats = {}
        for i, s in enumerate(user_info[4:10]):
            u_stats[util.STATS_LIST[i]] = float(s)
        if move.effects.rdm_move:
            if move.name != 'Sleep Talk' or (move.name == 'Sleep Talk' and user_info[4] == util.SLP):
                user_moves.remove(move)
                if user_moves:
                    move = choice(user_moves)
        dmg = self.damage_calc(user_info[:2], move, target_info[:2], target_info[2], target_info[3], u_stats,
                               target_info[4:10], field_info[8:10], field_info[4:8])
        if move.move_type == util.STATUS or dmg > 0.0:
            for s in move.effects.stat_change:
                if s[0] == util.STATS_CLEAR:
                    user_info[5:10] = user_base
                    if s[1] != util.T_USER and field_info[15] == 0:
                        target_info[5:10] = target_base
                elif s == util.STAT_STEAL:
                    # TODO Stat steal
                    pass
                else:
                    if s[3] and random() > 0.25:
                        continue
                    stat_index = util.STATS_LIST.index(s[0]) - 1
                    stage = int(s[2])
                    if s[1] == util.T_USER:
                        if user_info[2] == 'Contrary':
                            stage *= -1
                        if side == self.Driver.SELF_SIDE:
                            self.P_STAT_STAGES[stat_index] = max(-6, min(6, stage + self.P_STAT_STAGES[stat_index]))
                            new_stage = self.P_STAT_STAGES[stat_index]
                        else:
                            self.O_STAT_STAGES[stat_index] = max(-6, min(6, stage + self.O_STAT_STAGES[stat_index]))
                            new_stage = self.O_STAT_STAGES[stat_index]
                        user_info[stat_index + 5] = calc_stat_by_stage(float(user_base[stat_index]), new_stage)
                    elif field_info[15] == 0:
                        if target_info[2] == 'Contrary':
                            stage *= -1
                        if side == self.Driver.SELF_SIDE:
                            self.O_STAT_STAGES[stat_index] = max(-6, min(6, stage + self.O_STAT_STAGES[stat_index]))
                            new_stage = self.P_STAT_STAGES[stat_index]
                        else:
                            self.P_STAT_STAGES[stat_index] = max(-6, min(6, stage + self.P_STAT_STAGES[stat_index]))
                            new_stage = self.P_STAT_STAGES[stat_index]
                        target_info[stat_index + 5] = calc_stat_by_stage(float(target_base[stat_index]), new_stage)
            if user_info[3] == 'White Herb':
                if side == self.Driver.SELF_SIDE:
                    if any(s < 0 for s in self.P_STAT_STAGES):
                        for s, i in enumerate(self.P_STAT_STAGES):
                            if s < 0:
                                self.P_STAT_STAGES[i] = 0
                                user_info[i + 5] = calc_stat_by_stage(float(user_base[i]), 0)
                        user_info[3] = ''
                else:
                    if any(s < 0 for s in self.O_STAT_STAGES):
                        for s, i in enumerate(self.O_STAT_STAGES):
                            if s < 0:
                                self.O_STAT_STAGES[i] = 0
                                user_info[i + 5] = calc_stat_by_stage(float(user_base[i]), 0)
                        user_info[3] = ''
            if target_info[3] == 'White Herb':
                if side == self.Driver.OPP_SIDE:
                    if any(s < 0 for s in self.P_STAT_STAGES):
                        for s, i in enumerate(self.P_STAT_STAGES):
                            if s < 0:
                                self.P_STAT_STAGES[i] = 0
                                target_info[i + 5] = calc_stat_by_stage(float(target_base[i]), 0)
                        target_info[3] = ''
                else:
                    if any(s < 0 for s in self.O_STAT_STAGES):
                        for s, i in enumerate(self.O_STAT_STAGES):
                            if s < 0:
                                self.O_STAT_STAGES[i] = 0
                                target_info[i + 5] = calc_stat_by_stage(float(target_base[i]), 0)
                        target_info[3] = ''
            if move.effects.crit is not None:
                if not move.effects.crit or random() <= 0.125:
                    dmg *= 1.5
            if move.effects.status:
                if not move.effects.status[2] or random() <= 0.25:
                    if move.effects.status[1] == util.T_USER:
                        if move.effects.status[0] == util.CONFUSED:
                            user_info[-1] = move.effects.status[0]
                        else:
                            if move.name == 'Rest' \
                                    or status_can_effect(move.effects.status[0], user_info[0:3], user_info[-2]):
                                user_info[-2] = move.effects.status[0]
                    elif field_info[15] == 0:
                        if target_info[2] == 'Magic Bounce':
                            if move.effects.status[0] == util.CONFUSED:
                                user_info[-1] = move.effects.status[0]
                            else:
                                if status_can_effect(move.effects.status[0], user_info[0:3], user_info[-2]):
                                    user_info[-2] = move.effects.status[0]
                        else:
                            if move.effects.status[0] == util.CONFUSED:
                                target_info[-1] = move.effects.status[0]
                            else:
                                if status_can_effect(move.effects.status[0], target_info[0:3], target_info[-2]):
                                    target_info[-2] = move.effects.status[0]
            if move.effects.field:
                field_index = 0 if target_info[2] == 'Magic Bounce' else 8
                field_info = update_field(move, field_info, field_index)
                if move.effects.field == util.FIELD_SUBSTITUTE:
                    if side == self.Driver.SELF_SIDE:
                        self.P_SUB_HP = user_base_hp * 0.25
                    else:
                        self.O_SUB_HP = user_base_hp * 0.25
            if move.effects.weather:
                field_info[16] = move.effects.weather
            if move.effects.terrain:
                field_info[17] = move.effects.terrain
            if move.effects.recoil:
                user_info[4] = max(0.0, min(float(user_info[4]) - (float(move.effects.recoil) / 100.0) * dmg,
                                            user_base_hp))
            if move.effects.cure:
                if move.effects.cure == util.T_USER:
                    user_info[-1], user_info[-2] = '', ''
                if move.effects.cure == util.T_OPP and field_info[15] == 0:
                    target_info[-1], target_info[-2] = '', ''
                # TODO Team, All, Switch
            if move.effects.item_remove:
                target_info[3] = ''
            if move.effects.pain_split and field_info[15] == 0:
                split_hp = (float(user_info[4]) + float(target_info[4])) / 2.0
                user_info[4], target_info[4] = split_hp, split_hp
            if move.effects.trick:
                u_item, t_item = user_info[3], target_info[3]
                user_info[3], target_info[3] = t_item, u_item
            if move.effects.lvl_dmg:
                target_info[4] = max(0.0, float(target_info[4]) - 82.0)
            if move.effects.endeavor and field_info[15] == 0:
                target_info[4] = user_info[4]
            if move.effects.type_change and field_info[15] == 0:
                if move.effects.type_change[0] == util.T_USER:
                    user_info[0], user_info[1] = move.effects.type_change[1], ''
                else:
                    target_info[0], target_info[1] = move.effects.type_change[1], ''
            if move.effects.flinch is not None:
                # TODO Fake Out
                target_effects[1] = not move.effects.flinch or random() <= 0.15
            if move.effects.protect:
                target_effects[2] = True
            if move.effects.counter:
                target_effects[0] = move.effects.counter
            if move.effects.switch:
                if move.effects.switch == util.T_OPP:
                    target_effects[4] = True
                else:
                    user_effects[0] = True
            if move.effects.charge:
                if move.name == 'Solar Beam':
                    user_effects[2] = field_info[16] != util.W_SUN and field_info[16] != util.W_HARSH_SUN
                else:
                    if user_info[3] == 'Power Herb':
                        user_info[3] = ''
                    else:
                        user_effects[2] = True
            if move.effects.recharge:
                user_effects[1] = True
            if move.effects.contact_dmg:
                target_effects[3] = True
            if move.effects.levitate:
                target_effects[5] = True
            if move.effects.move_lock:
                if move.effects.move_lock == util.T_USER:
                    user_effects[3] = True
                    move_lock = util.T_USER
                else:
                    target_effects[6] = True
                    move_lock = util.T_OPP
            if move.effects.heal:
                # TODO Destiny Bond
                # TODO Wish
                if not move.effects.heal[2]:
                    if move.effects.heal[0] == util.T_USER:
                        user_info[4] = max(0.0, min(float(user_info[4]) + (user_base_hp * float(move.effects.heal[1])),
                                                    user_base_hp))
                    elif move.effects.heal[0] == util.T_OPP and field_info[15] == 0:
                        target_info[4] = max(0.0, float(target_info[4]) +
                                             (target_base_hp * float(move.effects.heal[1])))
                    # TODO Switch
            if side == self.Driver.OPP_SIDE:
                field_info = field_info[8:16] + field_info[:8] + field_info[16:19] + [field_info[20], field_info[19]]
        return user_info, target_info, field_info, dmg, (user_effects, target_effects, move_lock)

    def entry_hazards(self, cond, f_base, i_base):
        if i_base == 0:
            poke = self.get_poke(cond)
            base_hp = float(poke.stats[util.HP])
            base_spe = float(poke.stats[util.SPE])
        else:
            base_hp = float(self.battle_logger.stats_map[cond[73]][0])
            base_spe = float(self.battle_logger.stats_map[cond[73]][5])
        if cond[f_base] != 0:
            if not any(t == util.FLYING for t in cond[i_base + 1:i_base + 3]):
                cond[i_base + 5] = max(0.0, float(cond[i_base + 5]) - (base_hp * (2.080 * (cond[f_base] ^ 2))
                                                                       - (2.07 * cond[f_base]) + 12.49))
        if cond[f_base + 1] != 0:
            effectiveness = 12.5
            for t in cond[i_base + 1: i_base + 3]:
                effectiveness *= util.type_effectiveness(util.ROCK, t)
        if cond[f_base + 2] != 0:
            if any(t == util.POISON for t in cond[i_base + 1:i_base + 3]):
                if cond[i_base + 3] != 'Levitate' and not any(t == util.FLYING for t in cond[i_base + 1:i_base + 3]):
                    cond[f_base + 2] = 0
            elif cond[i_base + 3] != 'Levitate' \
                    and not any((t == util.FLYING or t == util.STEEL) for t in cond[i_base + 1:i_base + 3]) \
                    and cond[i_base + 11] == '':
                if cond[f_base + 2] == 1:
                    cond[i_base + 11] = util.PSN
                else:
                    cond[i_base + 11] = util.TOX
        if cond[i_base + 4] == 'Sitrus Berry' and 0.0 < float(cond[i_base + 5]) <= base_hp * 0.5:
            cond[i_base + 5] = float(cond[i_base + 5]) + (base_hp * 0.25)
            cond[i_base + 4] = ''
        if cond[f_base + 3] != 0 and not any(t == util.FLYING for t in cond[i_base + 1:i_base + 3]) \
                and cond[i_base + 3] != 'Levitate' and cond[i_base + 4] != 'Air Balloon':
            stage = 1
            if cond[i_base + 3] == 'Contrary':
                stage *= -1
            if i_base == 0:
                self.P_STAT_STAGES[4] = stage
            else:
                self.O_STAT_STAGES[4] = stage
            cond[i_base + 10] = calc_stat_by_stage(base_spe, stage)

    def player_switch(self, cond, p_a):
        switch_choice = None
        if p_a is None:
            p_team_copy = []
            for p in self.battle_logger.self_team:
                if cond[0] != p.name and p.name in cond[:73] and float(cond[cond.index(p.name) + 5]) > 0.0:
                    p_team_copy.append(p)
            if p_team_copy:
                switch_choice = choice(p_team_copy)
        else:
            switch_choice = p_a[1]
        if any(cond[(index := 13 + (i * 12))] == switch_choice for i in range(5)):
            poke = self.get_poke(cond)
            old_active_values = cond[:6] + [poke.stats[s] for s in util.STATS_LIST[1:]] + [cond[11]]
            new_active_values = cond[index:index + 12]
            # print(old_active_values)
            # print(new_active_values)
            cond[:12] = new_active_values
            cond[12] = ''
            cond[index:index + 12] = old_active_values
            self.P_STAT_STAGES = [0] * 5
            self.entry_hazards(cond, 146, 0)
            self.P_SUB_HP = 0.0
            # print('Post-switch method:', cond)

    def player_switch_move(self, cond):
        switch = self.party_options(get_names=True)
        if any((poke := p)[1] == cond[0] for p in switch):
            switch.remove(poke)
        # switch.sort(key=lambda v: v[1])
        return cond, switch, []

    def player_attack(self, cond, p_a, o_a=None, o_dmg=0):
        effects = ([False, False, False, False], ['', False, False, False, False, False, False], False)
        if p_a[1].name != 'Sucker Punch' \
                or (o_a and o_a not in self.battle_logger.stats_map and o_a.move_type != util.STATUS):
            poke = self.get_poke(cond)
            moves = [self.battle_logger.move_map[m] for m in poke.moves]
            cond[1:13], cond[74:86], cond[146:], dmg, effects = self.dmg_effects(self.Driver.SELF_SIDE, p_a[1], cond,
                                                                                 moves)
            if o_a is not None:
                if o_a not in self.battle_logger.stats_map:
                    if effects[1][0] == o_a.move_type:
                        dmg = o_dmg * 2
            if cond[61] == 1:
                self.O_SUB_HP = max(0.0, self.O_SUB_HP - dmg)
                if self.O_SUB_HP <= 0.0:
                    cond[61] = 0
            else:
                cond[78] = max(0.0, float(cond[78]) - dmg)
                if cond[77] == 'Sitrus Berry':
                    if 0.0 < float(cond[78]) <= float(self.battle_logger.stats_map[cond[73]][0]) * 0.5:
                        cond[78] = float(cond[78]) + (float(self.battle_logger.stats_map[cond[73]][0]) * 0.25)
                        cond[77] = ''
            if cond[4] == 'Life Orb' and dmg > 0.0:
                base_hp = float(poke.stats[util.HP])
                cond[5] = max(0.0, float(cond[5]) - base_hp * 0.1)
        return effects

    def opp_switch(self, cond, o_a):
        o_switch = None
        if not o_a:
            opp_team_copy = self.get_opp_team_copy(cond)
            if opp_team_copy:
                p = choice(opp_team_copy)
                o_switch = p.name
        else:
            o_switch = o_a
        if o_switch and any(cond[(index := 86 + (i * 12))] == o_switch for i in range(5)):
            # print('Before 1:', cond)
            if cond[73] == '':
                old_active_values = cond[73:85]
            else:
                stats = self.battle_logger.stats_map[cond[73]]
                old_active_values = cond[73:79] + [stats[i + 1] for i in range(5)] + [cond[84]]
            new_active_values = cond[index:index + 12]
            cond[73:85] = new_active_values
            cond[85] = ''
            cond[index:index + 12] = old_active_values
            self.O_STAT_STAGES = [0] * 5
            self.entry_hazards(cond, 154, 73)
            self.O_SUB_HP = 0.0
            # print('After 1:', cond)

    def get_poke(self, cond):
        poke = None
        for p in self.battle_logger.self_team:
            if p.name == cond[0]:
                poke = p
                break
        return poke

    def get_switch(self, cond):
        switch = self.party_options(get_names=True)
        if any((poke2 := p)[1] == cond[0] for p in switch):
            switch.remove(poke2)
        # switch.sort(key=lambda v: v[1])
        return switch

    def get_o_poke_and_moves(self, cond, o_move):
        o_poke = None
        for p in self.battle_logger.opp_team:
            if p.name == cond[73]:
                o_poke = p
                break
        if o_poke is None and o_move and o_move not in self.battle_logger.stats_map:
            return o_poke, [o_move]
        o_moves = [self.battle_logger.move_map[m] for m in o_poke.moves]
        if o_move and o_move not in self.battle_logger.stats_map and o_move not in o_moves:
            o_moves.append(o_move)
        o_moves = self.rand_moves(o_moves, cond[73])
        return o_poke, o_moves

    def get_opp_team_copy(self, cond):
        opp_team_copy = []
        for p in self.battle_logger.opp_team:
            if p.name in cond[73:]:
                team_index = cond.index(p.name)
                if cond[73] != p.name and float(cond[team_index + 5]) > 0.0:
                    opp_team_copy.append(p)
        return opp_team_copy

    def post_turn_effects(self, cond, idx):
        if cond[idx] != '' and float(cond[idx + 5]) > 0.0:
            base_hp = float(self.battle_logger.stats_map[cond[idx]][0])
            if cond[idx + 4] == 'Leftovers' or (cond[idx + 4] == 'Black Sludge'
                                                and (cond[idx + 1] == util.POISON or cond[idx + 2] == util.POISON)):
                cond[idx + 5] = min(float(cond[idx + 5]) + base_hp * 0.0625, 100.0)
            if cond[idx + 11] == util.TOX:
                if idx == 0:
                    count = self.P_TOX
                else:
                    count = self.O_TOX
                cond[idx + 5] = max(0.0, float(cond[idx + 5]) - base_hp * (count / 16.0))
            if cond[idx + 11] == util.BRN or cond[idx + 11] == util.PSN:
                cond[idx + 5] = max(0.0, float(cond[idx + 5]) - base_hp * 0.0625)
            types = cond[idx + 1:idx + 3]
            if (cond[162] == util.W_SANDSTORM
                and util.GROUND not in types and util.ROCK not in types and util.STEEL not in types) \
                    or (cond[162] == util.W_HAIL and util.ICE not in types):
                cond[idx + 5] = max(0.0, float(cond[idx + 5]) - base_hp * 0.0625)
            if 0.0 < float(cond[idx + 5]) < base_hp * 0.5 and cond[idx + 4] == 'Sitrus Berry':
                cond[idx + 5] = float(cond[idx + 5]) + base_hp * 0.25
                cond[idx + 4] = ''

    def fp_check(self, user_move, target_move):
        if target_move in self.battle_logger.stats_map:
            return True
        if user_move.name != 'Focus Punch':
            return True
        return target_move.move_type == util.STATUS

    def build_node(self, node_list, i, node, p_a, o_a):
        new_node = Node(len(node_list) + i, node.id, p_act=p_a, opp_act=o_a,
                        cond_act=self.get_cond_act(p_a, o_a, node.conditions))
        new_node.value = self.calc_value(new_node, node_list)
        return new_node

    def calc_node_value_and_children(self, node, node_list):
        # TODO Comparison function
        if not node.opp_actions:
            actions = list(product(node.player_actions, [None]))
        else:
            actions = list(product(node.player_actions, node.opp_actions))
        nodes = Parallel(n_jobs=num_cores, backend='threading')(delayed(self.build_node)(node_list, i, node, a[0], a[1])
                                                                for i, a in enumerate(actions))
        nodes.sort(key=lambda n: n.id)
        node.children.extend(nodes)
        return node

    def calc_value(self, node, node_list):
        new_cond = node.conditions
        old_cond = node_list[node.parent_id].conditions

        player_party = [(old_cond[0], 0)]
        opp_party = [(old_cond[73], 73)]
        opp_not_used = [(new_cond[73], 73)]
        for i in range(5):
            player_party.append((old_cond[13 + (12 * i)], 13 + (12 * i)))
            opp_party.append((old_cond[86 + (12 * i)], 86 + (12 * i)))
            opp_not_used.append((new_cond[86 + (12 * i)], 86 + (12 * i)))
        phc, ohc = 0.0, 0.0
        psc, osc = 0.0, 0.0
        ps, ost = 0.0, 0.0
        pca, oca = 6, 6
        pf, of = 0.0, 0.0

        for i in range(6):
            # Player
            player_p, idx = player_party[i]
            if player_p == new_cond[0]:
                for j in range(6):
                    stat = float(self.battle_logger.stats_map[player_p][j])
                    c = ((float(new_cond[5 + j]) / stat) - (float(old_cond[idx + 5 + j]) / stat)) * 10
                    if j == 0:
                        if float(new_cond[5]) <= 0.0:
                            pca -= 1
                        phc += c
                    else:
                        psc += c
                if idx == 0:
                    ps += util.calc_status_change(old_cond[11], new_cond[11], '')
                    ps += util.calc_status_change(old_cond[12], new_cond[12], '')
                else:
                    ps += util.calc_status_change(old_cond[idx + 11], new_cond[11], '')
                    ps += util.calc_status_change('', new_cond[12], '')
            else:
                for j in range(5):
                    if player_p == '':
                        continue
                    if player_p == new_cond[13 + (12 * j)]:
                        if float(old_cond[idx + 5]) <= 0.0:
                            pca -= 1
                        else:
                            for k in range(6):
                                stat = float(self.battle_logger.stats_map[player_p][k])
                                index = 18 + k + (12 * j)
                                c = ((float(new_cond[index]) / stat) - (float(old_cond[idx + 5 + k]) / stat)) * 10
                                if k == 0:
                                    if float(new_cond[index]) <= 0.0:
                                        pca -= 1
                                    phc += c * 2
                                else:
                                    psc += c
                            if idx == 0:
                                ps += util.calc_status_change(old_cond[11], new_cond[24 + (12 * j)], '')
                                ps += util.calc_status_change(old_cond[12], '', '')
                            else:
                                ps += util.calc_status_change(old_cond[idx + 11], new_cond[24 + (12 * j)], '')
                            break

            # Opp
            opp_p, opp_i = opp_party[i]
            if opp_p == '':
                continue
            if opp_p == new_cond[73]:
                opp_not_used.remove((new_cond[73], 73))
                if float(old_cond[opp_i + 5]) <= 0.0:
                    oca -= 1
                else:
                    f = False
                    for j in range(6):
                        stat = float(self.battle_logger.stats_map[opp_p][j])
                        c = ((float(old_cond[opp_i + 5 + j]) / stat) - (float(new_cond[78 + j]) / stat)) * 10
                        if j == 0:
                            ohc += c * 2
                            if float(new_cond[78]) <= 0.0:
                                oca -= 1
                                f = True
                                break
                        else:
                            osc += c
                    if not f:
                        if opp_i == 73:
                            ost += util.calc_status_change(new_cond[84], old_cond[84], '')
                            ost += util.calc_status_change(new_cond[85], old_cond[85], '')
                        else:
                            ost += util.calc_status_change(new_cond[84], old_cond[opp_i + 11], '')
                            ost += util.calc_status_change(new_cond[85], '', '')
                    continue
            for j in range(5):
                if opp_p == new_cond[86 + (12 * j)]:
                    opp_not_used.remove((new_cond[86 + (12 * j)], 86 + (12 * j)))
                    if float(old_cond[opp_i + 5]) <= 0.0:
                        oca -= 1
                    else:
                        f = False
                        for k in range(6):
                            index = 91 + k + (12 * j)
                            stat = float(self.battle_logger.stats_map[opp_p][k])
                            c = ((float(old_cond[opp_i + 5 + k]) / stat) - (float(new_cond[index]) / stat)) * 10
                            if k == 0:
                                ohc += c * 2
                                if float(new_cond[index]) <= 0.0:
                                    oca -= 1
                                    f = True
                                    break
                            else:
                                osc += c
                        if not f:
                            if opp_i == 73:
                                ost += util.calc_status_change(new_cond[98 + (12 * j)], old_cond[84], '')
                                ost += util.calc_status_change('', old_cond[85], '')
                            else:
                                ost += util.calc_status_change(new_cond[98 + (12 * j)], old_cond[opp_i + 11])
                        break
        for p, i in opp_not_used:
            if p == '':
                continue
            f = False
            for j in range(6):
                stat = float(self.battle_logger.stats_map[p][j])
                c = (1.0 - (float(new_cond[i + 5 + j]) / stat)) * 10
                if j == 0:
                    ohc += c * 2
                    if float(new_cond[i + 5]) <= 0.0:
                        oca -= 1
                        f = True
                        break
                else:
                    osc += c
            if not f:
                ost += util.calc_status_change(new_cond[i + 11], '', '')
                if i + 12 == 98:
                    ost += util.calc_status_change(new_cond[98], '', '')

        # Field changes
        for i in range(len(util.FIELD_LIST)):
            pf += util.calc_field_change(old_cond[146 + i], new_cond[146 + i], i)
            of += util.calc_field_change(new_cond[154 + i], old_cond[154 + i], i)

        pf += util.calc_field_change(old_cond[165], new_cond[165], 5, '')
        of += util.calc_field_change(new_cond[166], old_cond[166], 5, '')

        self.battle_logger.player_alive = pca
        self.battle_logger.opp_alive = oca
        if pca == 0:
            return -100
        if oca == 0:
            return 100
        return phc + (ohc * 1.5) + psc + osc + ps + ost + pf + of + (pca * 10) - (oca * 10)

    def filter_o_act(self, actions, cond):
        if len(actions) <= 1:
            return actions
        actions_copy = []
        for a in actions:
            if a in self.battle_logger.stats_map:
                actions_copy.append(a)
                continue
            if a.move_type == util.STATUS:
                if not self.filter_effects(a, cond, self.Driver.OPP_SIDE):
                    actions_copy.append(a)
                continue
            if a.type == util.IMMUNE_ABILITIES.get(cond[3], None):
                continue
            v = 1
            for t in cond[1:3]:
                v *= util.type_effectiveness(a.type, t)
            if v != 0:
                actions_copy.append(a)
        return actions_copy

    def filter_p_act(self, actions, cond):
        if len(actions) <= 1:
            return actions
        actions_copy = []
        for a in actions:
            if a[1] in self.battle_logger.stats_map:
                actions_copy.append(a)
                continue
            if a[1].move_type == util.STATUS:
                if not self.filter_effects(a[1], cond, self.Driver.SELF_SIDE):
                    actions_copy.append(a)
                continue
            if a[1].type == util.IMMUNE_ABILITIES.get(cond[76], None):
                continue
            v = 1
            for t in cond[74:76]:
                v *= util.type_effectiveness(a[1].type, t)
            if v != 0:
                actions_copy.append(a)
        return actions_copy

    def filter_effects(self, action, cond, side):
        if side == self.Driver.SELF_SIDE:
            target_info = cond[74:86]
            field_info = cond[146:]
            user_stages = self.P_STAT_STAGES
            target_stages = self.O_STAT_STAGES
        else:
            target_info = cond[1:13]
            field_info = cond[154:162] + cond[146:154] + cond[162:165] + [cond[166], cond[165]]
            user_stages = self.O_STAT_STAGES
            target_stages = self.P_STAT_STAGES
        if action.effects.status and action.effects.status[0] != util.CONFUSED\
                and action.effects.status[1] == util.T_OPP:
            return not status_can_effect(action.effects.status[0], target_info[:2], target_info[-1])
        for s in action.effects.stat_change:
            index = util.STATS_LIST.index(s[0]) - 1
            base = user_stages[index] if s[1] == util.T_USER else target_stages[index]
            if max(-6, min(6, base + int(s[2]))) == base:
                return True
        if action.effects.field:
            return copy(field_info) == update_field(action, field_info, 8)
        return False

    def __repr__(self):
        return 'MinMaxBot'
