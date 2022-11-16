from copy import copy
from random import random, choice
from re import match, search, findall

import numpy as np

from collections import deque
from time import time

from selenium.common import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By

from bots.BattleBot import BattleBot
from util import util


class Node:

    def __init__(self, nid, parent_id, val=0, p_act=-1, opp_act=-1, cond_act=None):
        self.id = nid
        self.parent_id = parent_id
        self.value = val
        self.children = []
        self.player_action, self.opp_action = p_act, opp_act
        if cond_act is None:
            self.conditions, self.player_actions, self.opp_actions = [], [], []
        else:
            self.conditions, self.player_actions, self.opp_actions = cond_act


class MinMaxBot(BattleBot):
    cond_val_table = {}
    P_LOCK, O_LOCK = 0, 0

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
        print(action)
        if action in self.battle_logger.stats_map:
            self.Driver.wait_and_click("//button[@name='chooseSwitch'][contains(text(), '{}')]".format(action),
                                       by=By.XPATH)
        else:
            _, has_z, mega_elm = self.move_options(do_mega=False)
            if 'z' in action[0]:
                self.choose_move('z' + action[0], has_z, mega_elm)
            else:
                if not has_z and mega_elm:
                    mega_elm[0].click()
                self.choose_move(str(action[0]), has_z, mega_elm)

    def min_max(self, root, run_time):
        node_list = [root]
        parent_index = 0
        action = root.player_action
        root = self.calc_node_value_and_children(root, node_list)
        node_list[0] = root
        queue = deque()
        queue.extend(root.children)
        node_list.extend(root.children)
        action_list = []
        for n in root.children:
            if n.player_action not in action_list:
                action_list.append(n.player_action)
        alt_action_list = []
        for a in action_list:
            if a[1] in self.battle_logger.stats_map:
                alt_action_list.append(a[1])
            else:
                alt_action_list.append(a[1].name)
        while queue and time() - run_time < 15:
            node = queue.popleft()
            print(node.id)
            node = self.calc_node_value_and_children(node, node_list)
            node_list[node.id] = node
            node_list.extend(node.children)
            if not any(n.parent_id == parent_index for n in queue):
                # Completed searching specific children, update parent's value
                sub_parent = parent_index
                while sub_parent != 0:
                    parent_node = node_list[sub_parent]
                    parent_node.value = sum(c.value for c in parent_node.children) / len(parent_node.children)
                    sub_parent = parent_node.parent_id
                action_sum_count = [(0, 0)] * len(action_list)
                for c in root.children:
                    if c.player_action[1] in self.battle_logger.stats_map:
                        action_index = alt_action_list.index(c.player_action[1])
                    else:
                        action_index = alt_action_list.index(c.player_action[1].name)
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
        if not prev_cond:
            cond = [''] * 167
            # TODO Get conditions from parent? At least conditions that haven't changed
            # TODO Optimize loops & AC
            # Actions
            switch = []
            count = 0
            fainted = self.active_fainted()
            while len(player_actions) == 0 and self.Driver.in_battle():
                if not fainted:
                    options, _, _ = self.move_options(modded=True, do_mega=False)
                    player_actions = options
                switch = self.party_options(get_names=True)
                switch.sort(key=lambda v: v[1])
                player_actions = player_actions + switch
                if len(player_actions) == 0:
                    count += 1
                    print('ERROR: Legal actions empty, trying again. Attempts:', count)
            opp_party = self.get_opp_party_status()
            opp_active = ''
            opp_moves = []
            if any('active' in (elem := e).get_attribute('aria-label') for e in opp_party):
                opp_active = self.get_opp_name()
                opp_moves = self.move_options(num=-1)
                opp_party.remove(elem)
                opp_moves.sort()
            opp_switch = []
            for e in opp_party:
                if 'fainted' not in (label := e.get_attribute('aria-label')):
                    opp_switch.append((label.split("(")[0].strip(), label, e))
            opp_switch.sort(key=lambda l: l[0])
            opp_actions = opp_moves + [n for n, _, _ in opp_switch]
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
            player_statuses = []
            if not fainted:
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
            if any((text := s.text) in util.STATUS_LIST for s in player_statuses):
                cond[11] = text
            if any(s.text == util.CONFUSED for s in player_statuses):
                cond[12] = util.CONFUSED

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
                if len(ability) == 1:
                    if '(base:' in ability[0]:
                        ability[0] = ability[0].split('(')[0].strip()
                    cond[76] = ability[0]
                if item != '' and 'None' not in item:
                    if match(util.ITEM_GENERAL, item):
                        item = search(util.ITEM_GENERAL, item).group(1)
                    cond[77] = item
                opp_statuses = self.get_statuses(self.Driver.OPP_SIDE)
                opp_stats = self.update_stats(self.battle_logger.stats_map.get(opp_active, ["1.0"] * 6),
                                              hp_mod=self.get_opp_hp(), stat_changes=opp_statuses, provided=False)
                for i in range(len(util.STATS_LIST)):
                    cond[78 + i] = opp_stats[i]
                if any((text := s.text) in util.STATUS_LIST for s in opp_statuses):
                    cond[84] = text
                if any(s.text == util.CONFUSED for s in opp_statuses):
                    cond[85] = util.CONFUSED
            # Opp Party
            for i, p in enumerate(opp_switch):
                cond[86 + (i * 12)] = p[0]
                opp_team_types = self.Driver.get_type(poke_elem=p[2])
                for j, t in enumerate(opp_team_types):
                    cond[87 + j + (i * 12)] = t
                opp_team_abilities, opp_team_item = self.get_ability_item(self.Driver.OPP_SIDE, sidebar=True, elem=p)
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
        else:
            # Calculated/assumed conditions
            cond = copy(prev_cond)
            effects = ([False, False, False, False], ['', False, False, False, False, False, False], False)
            o_eff = ([False, False, False, False], ['', False, False, False, False, False, False], False)
            dmg, o_dmg = 0, 0
            if self.player_goes_first(cond, p_a, o_a):
                if p_a:
                    if p_a[1] in self.battle_logger.stats_map:
                        self.player_switch(cond, p_a)
                    else:
                        effects = self.player_attack(cond, p_a)
                        if effects[0][0]:
                            return self.player_switch_move(cond)
                if float(cond[79]) > 0.0:
                    if effects[1][4]:
                        self.opp_switch(cond, None)
                    elif o_a in self.battle_logger.stats_map:
                        self.opp_switch(cond, o_a)
                    elif not effects[1][1] and o_a:
                        # Attack
                        o_move = self.battle_logger.move_map[o_a]
                        o_poke, o_moves = self.get_o_poke_and_moves(cond)
                        if (not effects[1][2] or o_move.move_type == util.STATUS) and \
                                (not effects[1][5] or o_move.type != util.GROUND or o_move.move_type == util.STATUS):
                            cond[74:87], cond[1:13], cond[146:], o_dmg, o_eff = self.dmg_effects(self.Driver.OPP_SIDE,
                                                                                                 o_move, cond, o_moves)
                            if p_a[1] not in self.battle_logger.stats_map:
                                if o_eff[1][0] == p_a[1].move_type:
                                    o_dmg = dmg * 2
                            cond[5] = float(cond[5]) - o_dmg
                            base_hp = float(self.battle_logger.stats_map[cond[73]][0])
                            if cond[78] == 'Life Orb' and o_dmg > 0.0:
                                cond[79] = str(float(cond[79]) - base_hp * 0.1)
                            if effects[1][3] and o_move.move_type == util.PHYSICAL:
                                cond[79] = str(float(cond[79]) - base_hp * 0.125)
                            if o_eff[1][4]:
                                self.player_switch(cond, None)
                            if o_eff[0][0]:
                                self.opp_switch(cond, None)
            else:
                if o_a in self.battle_logger.stats_map:
                    self.opp_switch(cond, o_a)
                else:
                    # Attack
                    o_move = self.battle_logger.move_map[o_a]
                    o_poke, o_moves = self.get_o_poke_and_moves(cond)
                    cond[74:87], cond[1:13], cond[146:], o_dmg, o_eff = self.dmg_effects(self.Driver.OPP_SIDE,
                                                                                         o_move, cond, o_moves)
                    cond[5] = float(cond[5]) - o_dmg
                    if cond[78] == 'Life Orb' and o_dmg > 0.0:
                        base_hp = float(self.battle_logger.stats_map[cond[73]][0])
                        cond[79] = str(float(cond[79]) - base_hp * 0.1)
                    if o_eff[0][1]:
                        self.opp_switch(cond, None)
                    if float(cond[5]) > 0.0:
                        if o_eff[1][4]:
                            self.player_switch(cond, None)
                        elif p_a[1] in self.battle_logger.stats_map:
                            self.player_switch(cond, p_a)
                        elif not o_eff[1][1] and p_a:
                            # Attack
                            if (not o_eff[1][2] or p_a[1].move_type == util.STATUS) and \
                                    (not o_eff[1][5] or p_a[1].type != util.GROUND or p_a[1].move_type == util.STATUS):
                                effects = self.player_attack(cond, p_a, o_a, o_dmg)
                                if o_eff[1][3] and p_a[1].move_type == util.PHYSICAL:
                                    base_hp = float(self.battle_logger.stats_map[cond[0]][0])
                                    cond[5] = str(float(cond[5]) - base_hp * 0.125)
                                if o_eff[1][4]:
                                    self.opp_switch(cond, None)
                                if effects[0][0]:
                                    return self.player_switch_move(cond)
            self.post_turn_effects(cond, 0)
            self.post_turn_effects(cond, 73)
            p_fainted, o_fainted = float(cond[5]) <= 0.0, float(cond[79]) <= 0.0
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
                moves = [('', self.battle_logger.move_map[m]) for m in poke.moves]
                player_actions = moves + self.get_switch(cond)
            if o_fainted:
                opp_actions = self.get_opp_team_copy(cond)
            elif o_eff[0][1]:
                opp_actions = []
            elif o_eff[0][2] or self.O_LOCK > 0:
                opp_actions = [o_a]
            else:
                o_poke, o_moves = self.get_o_poke_and_moves(cond)
                opp_actions = o_moves + self.get_opp_team_copy(cond)
        return cond, player_actions, opp_actions

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
        o_move = self.battle_logger.move_map[o_a]
        # Priority
        if p_a[1].effects.priority > o_move.effects.priority:
            return True
        elif p_a[1].effects.priority < o_move.effects.priority:
            return False
        # Speed Check
        p_spd = float(conditions[10]) * 2 if conditions[165] else float(conditions[10])
        o_spd = float(conditions[83]) * 2 if conditions[166] else float(conditions[83])
        if conditions[164] != '':
            return p_spd >= o_spd
        else:
            return p_spd <= o_spd

    def dmg_effects(self, side, move, cond, user_moves):
        if side == self.Driver.SELF_SIDE:
            user_info = cond[1:13]
            target_info = cond[74:87]
            field_info = cond[146:]
        else:
            user_info = cond[74:87]
            target_info = cond[1:13]
            field_info = cond[154:162] + cond[146:154] + cond[162:165] + cond[166] + cond[165]
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
            user_moves.remove(move)
            if user_moves:
                move = choice(user_moves)
        dmg = self.damage_calc(user_info[:2], move, target_info[:2], target_info[2], target_info[3], u_stats,
                               target_info[4:10])
        for s in move.effects.stat_change:
            if s[0] == util.STATS_CLEAR:
                if side == self.Driver.SELF_SIDE:
                    self_info = self.get_poke(cond)
                    user_base = self_info
                    target_base = {}
                    target_stats = self.battle_logger.stats_map[cond[72]]
                    for i, st in enumerate(util.STATS_LIST):
                        target_base[st] = target_stats[i]
                else:
                    self_info = None
                    for p in self.battle_logger.self_team:
                        if p.name == cond[0]:
                            self_info = p
                            break
                    target_base = self_info
                    user_base = {}
                    user_stats = self.battle_logger.stats_map[cond[72]]
                    for i, st in enumerate(util.STATS_LIST):
                        user_base[st] = user_stats[i]
                user_info = self.get_stat_diff(side, user_base, user_info)
                if s[1] != util.T_USER:
                    if side == self.Driver.SELF_SIDE:
                        target_info = self.get_stat_diff(self.Driver.OPP_SIDE, target_base, target_info)
                    else:
                        pass
            else:
                if s[3] and random() > 0.25:
                    continue
                stat_index = 4 + util.STATS_LIST.index(s[0])
                if s[1] == util.T_USER:
                    stat = float(user_info[stat_index])
                    user_info[stat_index] = stat + stat * int(s[2]) * 0.268
                else:
                    stat = float(target_info[stat_index])
                    target_info[stat_index] = stat + stat * int(s[2]) * 0.268
        if move.effects.crit is not None:
            if not move.effects.crit or random() <= 0.125:
                dmg *= 1.5
        if move.effects.status:
            if not move.effects.status[2] or random() <= 0.25:
                if move.effects.status[1] == util.T_USER:
                    if move.effects.status[0] == util.CONFUSED:
                        user_info[-1] = move.effects.status[0]
                    else:
                        user_info[-2] = move.effects.status[0]
                else:
                    if move.effects.status[0] == util.CONFUSED:
                        target_info[-1] = move.effects.status[0]
                    else:
                        target_info[-2] = move.effects.status[0]
        if move.effects.field:
            if move.effects.field == util.SCREEN_CLEAR:
                field_info[12:15] = [0] * 3
            elif move.effects.field == util.FIELD_CLEAR:
                field_info[:4] = [0] * 4
            elif move.effects.field == util.W_TRICK_ROOM:
                field_info[-3] = util.W_TRICK_ROOM
            elif move.effects.field == util.W_TAILWIND:
                field_info[-2] = util.W_TAILWIND
            elif move.effects.field in util.FIELD_LIST[:4]:
                field_info[8 + util.FIELD_LIST.index(move.effects.field)] += 1
            elif move.effects.field in util.FIELD_LIST:
                field_info[util.FIELD_LIST.index(move.effects.field)] += 1
        if move.effects.weather:
            field_info[16] = move.effects.weather
        if move.effects.terrain:
            field_info[17] = move.effects.terrain
        if move.effects.recoil:
            user_info[4] = float(user_info[4]) - (float(move.effects.recoil) / 100.0) * dmg
        if move.effects.cure:
            if move.effects.cure == util.T_USER:
                user_info[-1], user_info[-2] = '', ''
            if move.effects.cure == util.T_OPP:
                target_info[-1], target_info[-2] = '', ''
            # TODO Team, All
        if move.effects.item_remove:
            target_info[3] = ''
        if move.effects.pain_split:
            split_hp = (float(user_info[4]) + float(target_info[4])) / 2.0
            user_info[4], target_info[4] = split_hp, split_hp
        if move.effects.trick:
            u_item, t_item = user_info[3], target_info[3]
            user_info[3], target_info[3] = t_item, u_item
        if move.effects.lvl_dmg:
            target_info[4] = float(target_info[4]) - 82.0
        if move.effects.endeavor:
            target_info[4] = user_info[4]
        if move.effects.type_change:
            if move.effects.type_change[0] == util.T_USER:
                user_info[0], user_info[1] = move.effects.type_change[1], ''
            else:
                target_info[0], target_info[1] = move.effects.type_change[1], ''
        if move.effects.flinch is not None:
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
        if side == self.Driver.OPP_SIDE:
            field_info = field_info[8:16] + field_info[:8] + field_info[16:19] + field_info[21] + field_info[20]
        return user_info, target_info, field_info, dmg, (user_effects, target_effects, move_lock)

    def player_switch(self, cond, p_a):
        switch_choice = None
        poke = self.get_poke(cond)
        if p_a is None:
            p_team_copy = []
            for p in self.battle_logger.self_team:
                if cond[0] != p.name and float(cond[cond.index(p.name) + 5]) > 0.0:
                    p_team_copy.append(p)
            if p_team_copy:
                switch_choice = choice(p_team_copy)
        else:
            switch_choice = p_a[1]
        if switch_choice is not None:
            old_active_values = cond[:6] + [poke.stats[s] for s in util.STATS_LIST[1:]] + [cond[11]]
            new_active_values = [''] * 12
            if any(cond[(index := 13 + (i * 12))] == switch_choice for i in range(5)):
                new_active_values = cond[index:index + 12]
            cond[:12] = new_active_values
            cond[12] = ''
            cond[index:index + 12] = old_active_values

    def player_switch_move(self, cond):
        switch = self.party_options(get_names=True)
        if any((poke := p)[1] == cond[0] for p in switch):
            switch.remove(poke)
        switch.sort(key=lambda v: v[1])
        return cond, switch, []

    def player_attack(self, cond, p_a, o_a=None, o_dmg=0):
        poke = self.get_poke(cond)
        moves = [self.battle_logger.move_map[m] for m in poke.moves]
        cond[1:13], cond[74:87], cond[146:], dmg, effects = self.dmg_effects(self.Driver.SELF_SIDE,
                                                                             p_a[1], cond, moves)
        if o_a is not None:
            if o_a not in self.battle_logger.stats_map:
                if effects[1][0] == o_a.move_type:
                    dmg = o_dmg * 2
        cond[79] = float(cond[79]) - dmg
        if cond[4] == 'Life Orb' and dmg > 0.0:
            base_hp = float(self.battle_logger.stats_map[cond[0]][0])
            cond[5] = str(float(cond[5]) - base_hp * 0.1)
        return effects

    def opp_switch(self, cond, o_a):
        o_switch = None
        if o_a is None:
            opp_team_copy = self.get_opp_team_copy(cond)
            if opp_team_copy:
                o_switch = choice(opp_team_copy)
        else:
            o_switch = o_a
        if o_switch is not None:
            stats = self.battle_logger.stats_map[cond[73]]
            old_active_values = cond[73:79] + [stats[s] for s in util.STATS_LIST[1:]] + [cond[84]]
            new_active_values = [''] * 12
            if any(cond[(index := 86 + (i * 12))] == o_switch for i in range(5)):
                new_active_values = cond[index:index + 12]
            cond[73:85] = new_active_values
            cond[85] = ''
            cond[index:index + 12] = old_active_values

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
        switch.sort(key=lambda v: v[1])
        return switch

    def get_o_poke_and_moves(self, cond):
        o_poke = None
        for p in self.battle_logger.opp_team:
            if p.name == cond[73]:
                o_poke = p
                break
        o_moves = [self.battle_logger.move_map[m] for m in o_poke.moves]
        return o_poke, o_moves

    def get_opp_team_copy(self, cond):
        opp_team_copy = []
        for p in self.battle_logger.opp_team:
            team_index = cond.index(p.name)
            if cond[73] != p.name and float(cond[team_index + 5]) > 0.0:
                opp_team_copy.append(p)
        return opp_team_copy

    def post_turn_effects(self, cond, idx):
        if float(cond[idx + 5]) > 0.0:
            base_hp = float(self.battle_logger.stats_map[cond[idx]][0])
            if cond[idx + 4] == 'Leftovers' or (cond[idx + 4] == 'Black Sludge'
                                                and (cond[idx + 1] == util.POISON or cond[idx + 2] == util.POISON)):
                cond[idx + 5] = str(min(float(cond[idx + 5]) + base_hp * 0.0625, 100.0))
            if cond[idx + 11] == util.BRN or cond[idx + 11] == util.PSN:
                cond[idx + 5] = str(float(cond[idx + 5]) - base_hp * 0.0625)

    def calc_node_value_and_children(self, node, node_list):
        if node.parent_id != -1:
            # TODO Comparison function
            node.value = self.calc_value(node, node_list)
            # node.value = self.cond_val_table.get(node.conditions, self.calc_value(node, node_list))
            # self.cond_val_table[node.conditions] = node.value
        i = 0
        for p_a in node.player_actions:
            if node.opp_actions:
                for o_a in node.opp_actions:
                    node.children.append(Node(len(node_list) + i, node.id, p_act=p_a, opp_act=o_a,
                                              cond_act=self.get_cond_act(p_a, o_a, node.conditions)))
                    i += 1
            else:
                node.children.append(Node(len(node_list) + i, node.id, p_act=p_a,
                                          cond_act=self.get_cond_act(p_a, None, node.conditions)))
                i += 1
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
        poa, ooa = self.battle_logger.player_alive, self.battle_logger.opp_alive
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
                if old_cond[opp_i + 5] <= 0.0:
                    oca -= 1
                else:
                    f = False
                    for j in range(6):
                        stat = float(self.battle_logger.stats_map[opp_p][j])
                        c = ((float(old_cond[opp_i + 5 + j]) / stat) - (float(new_cond[78 + j]) / stat)) * 10
                        if j == 0:
                            ohc += c * 2
                            if float(new_cond[79]) <= 0.0:
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
                    if old_cond[opp_i + 5] <= 0.0:
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
            pf += util.calc_field_change(min(3, old_cond[146 + i]), min(3, new_cond[146 + i]), i)
            of += util.calc_field_change(min(3, new_cond[154 + i]), min(3, old_cond[154 + i]), i)

        pf += util.calc_field_change(old_cond[165], new_cond[165], 5, '')
        of += util.calc_field_change(new_cond[166], old_cond[166], 5, '')

        pa = pca - poa
        oa = ooa - oca
        self.battle_logger.player_alive = pca
        self.battle_logger.opp_alive = oca
        return phc + ohc + psc + osc + ps + ost + pf + of + (pa * 10) + (oa * 10)

    def __repr__(self):
        return 'MinMaxBot'
