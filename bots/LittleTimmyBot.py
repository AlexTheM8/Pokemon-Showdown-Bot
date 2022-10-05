from random import randrange

from selenium.webdriver.common.by import By

from bots.BattleBot import BattleBot
from util.BattleLogger import Move


class LittleTimmyBot(BattleBot):

    def choose_action(self):
        if self.active_fainted():
            self.choose_switch()
        else:
            options, has_z, mega_elem = self.move_options(modded=True)
            player_type, opponent_type = self.get_type(self.SELF_SIDE), self.get_type(self.OPPONENT_SIDE)
            ability, item = self.get_ability_item(self.OPPONENT_SIDE, do_ac=False)
            if 'None' in item:
                item = ''
            stats = self.get_stats(do_ac=False)
            strongest, pick = 0.0, options[randrange(len(options))][0]
            opp_stats = self.battle_logger.stats_map.get(self.get_opp_name(), ["1.0"] * 5)
            # TODO Get opp modifiers
            for v, m in options:
                if len(ability) > 1:
                    calc = self.damage_calc(player_type, m, opponent_type, '', item, stats, opp_stats)
                else:
                    calc = self.damage_calc(player_type, m, opponent_type, ability[0], item, stats, opp_stats)
                if calc > strongest:
                    strongest, pick = calc, v
            self.choose_move(pick, has_z, mega_elem)

    def best_pick(self):
        # TODO If opp fainted, calculate based on all known pokemon
        party = self.party_options()
        potential, pick = -10, party[randrange(len(party))]
        temp_elem = self.Driver.driver.find_elements(
            value="//div[@class='trainer trainer-far']/div[@class='teamicons']/span[@class='picon has-tooltip']",
            by=By.XPATH)
        if not any('active' in e.get_attribute('aria-label') for e in temp_elem):
            return pick
        opp_type = self.get_type(self.OPPONENT_SIDE)
        ability, item = self.get_ability_item(self.OPPONENT_SIDE, do_ac=False)
        opp_stats = ["1.0"] * 5
        if 'None' in item:
            item = ''
        for p in party:
            poke_type = self.get_type(self.SELF_SIDE, int(p))
            poke_ability, p_item = self.get_ability_item(self.SELF_SIDE, num=p, do_ac=False)
            if 'None' in p_item:
                p_item = ''
            calc = 0.0
            for t in poke_type:
                move = Move(t=t, base_power=1.0)
                if len(ability) > 1:
                    calc += self.damage_calc(poke_type, move, opp_type, '', item, {}, opp_stats)
                else:
                    calc += self.damage_calc(poke_type, move, opp_type, ability[0], item, {}, opp_stats)
            for t in opp_type:
                calc -= self.damage_calc(opp_type, Move(t=t, base_power=1.0), poke_type, poke_ability, p_item, {},
                                         opp_stats)
            if calc > potential:
                potential, pick = calc, p
        return pick
