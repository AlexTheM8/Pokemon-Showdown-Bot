from random import randrange
from re import match, search

from bots.BattleBot import BattleBot
from util import util
from util.BattleLogger import Move


class YoungsterJoeyBot(BattleBot):

    def choose_action(self):
        if self.active_fainted():
            self.choose_switch()
        else:
            options, has_z, mega_elem = self.move_options(modded=True)
            ply_type = self.Driver.get_type(self.Driver.SELF_SIDE)
            stats = self.get_stats(max_hp=False, do_ac=False)
            opp_type = self.Driver.get_type(self.Driver.OPP_SIDE)
            ability, item = self.get_ability_item(self.Driver.OPP_SIDE, do_ac=False)
            if 'None' in item:
                item = ''
            if match(util.ITEM_FRISKED, item):
                item = search(util.ITEM_FRISKED, item).group(1)
            if match(util.ITEM_TRICKED, item):
                item = search(util.ITEM_TRICKED, item).group(1)
            strongest, pick = 0.0, options[randrange(len(options))][0]
            opp_stats = self.update_stats(self.battle_logger.stats_map.get(self.get_opp_name(), ["1.0"] * 6))
            weather = self.get_weather()
            opp_field = self.Driver.get_field_settings(self.Driver.OPP_SIDE)
            screens = [opp_field[f] for f in util.FIELD_LIST[4:7]]
            for v, m in options:
                if len(ability) > 1:
                    calc = self.damage_calc(ply_type, m, opp_type, '', item, stats, opp_stats, weather, screens)
                else:
                    calc = self.damage_calc(ply_type, m, opp_type, ability[0], item, stats, opp_stats, weather, screens)
                if calc > strongest:
                    strongest, pick = calc, v
            self.choose_move(pick, has_z, mega_elem)

    def best_pick(self):
        # TODO If opp fainted, calculate based on all known pokemon
        party = self.party_options()
        potential, pick = -10, party[randrange(len(party))]
        if not any('active' in e.get_attribute('aria-label') for e in self.get_opp_party_status()):
            return pick
        o_type = self.Driver.get_type(self.Driver.OPP_SIDE)
        ability, item = self.get_ability_item(self.Driver.OPP_SIDE, do_ac=False)
        opp_stats = ["1.0"] * 6
        if 'None' in item:
            item = ''
        if match(util.ITEM_FRISKED, item):
            item = search(util.ITEM_FRISKED, item).group(1)
        if match(util.ITEM_TRICKED, item):
            item = search(util.ITEM_TRICKED, item).group(1)
        for p in party:
            p_type = self.Driver.get_type(self.Driver.SELF_SIDE, int(p))
            poke_ability, p_item = self.get_ability_item(self.Driver.SELF_SIDE, num=p, do_ac=False)
            if 'None' in p_item:
                p_item = ''
            calc = 0.0
            weather = self.get_weather()
            opp_field = self.Driver.get_field_settings(self.Driver.OPP_SIDE)
            o_screens = [opp_field[f] for f in util.FIELD_LIST[4:7]]
            p_field = self.Driver.get_field_settings(self.Driver.SELF_SIDE)
            p_screens = [p_field[f] for f in util.FIELD_LIST[4:7]]
            for t in p_type:
                move = Move(t=t, base_power=1.0)
                if len(ability) > 1:
                    calc += self.damage_calc(p_type, move, o_type, '', item, {}, opp_stats, weather, o_screens)
                else:
                    calc += self.damage_calc(p_type, move, o_type, ability[0], item, {}, opp_stats, weather, o_screens)
            for t in o_type:
                calc -= self.damage_calc(o_type, Move(t=t, base_power=1.0), p_type, poke_ability, p_item, {},
                                         opp_stats, weather, p_screens)
            if calc > potential:
                potential, pick = calc, p
        return pick

    def __repr__(self):
        return 'LittleTimmyBot'
