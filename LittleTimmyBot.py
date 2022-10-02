from random import randrange

from selenium.webdriver.common.by import By

from BattleBot import BattleBot
from BattleLogger import Move


class LittleTimmyBot(BattleBot):

    def choose_action(self):
        if self.active_fainted():
            self.choose_switch()
        else:
            options, has_z, mega_elem = self.move_options(modded=True)
            poke_name = self.Driver.driver.find_element(value=self.ACTIVE_POKE_PATH, by=By.XPATH).text.split(',')[0]
            player_type, opponent_type = self.get_type(self.SELF_SIDE, num=1), self.get_type(self.OPPONENT_SIDE)
            ability, item = self.get_ability_item(self.OPPONENT_SIDE)
            stats = self.get_stats()
            for i, p in enumerate(self.battle_logger.self_team):
                if p.name == poke_name:
                    updated_poke = p
                    if p.moves is None:
                        updated_poke.set_moves(options)
                    # TODO Remove after updating get_stats
                    if p.stats is None:
                        updated_poke.stats = stats
                    self.battle_logger.self_team[i] = updated_poke
                    break
            strongest, pick = 0.0, options[randrange(len(options))][0]
            for v, m in options:
                if len(ability) > 1:
                    calc = self.damage_calc(player_type, m, opponent_type, '', '', stats)
                else:
                    calc = self.damage_calc(player_type, m, opponent_type, ability[0], '', stats)
                if calc > strongest:
                    strongest, pick = calc, v
            self.choose_move(pick, has_z, mega_elem)

    def best_pick(self):
        party = self.party_options()
        potential, pick = -10, party[randrange(len(party))]
        temp_elem = self.Driver.driver.find_elements(
            value="//div[@class='trainer trainer-far']/div[@class='teamicons']/span[@class='picon has-tooltip']",
            by=By.XPATH)
        if not any('active' in e.get_attribute('aria-label') for e in temp_elem):
            return pick
        opponent_type = self.get_type(self.OPPONENT_SIDE)
        ability, item = self.get_ability_item(self.OPPONENT_SIDE)
        for p in party:
            poke_type = self.get_type(self.SELF_SIDE, int(p))
            poke_ability, poke_item = self.get_ability_item(self.SELF_SIDE, num=p)
            calc = 0.0
            for t in poke_type:
                move = Move(t=t, base_power=1.0)
                if len(ability) > 1:
                    calc += self.damage_calc(poke_type, move, opponent_type, '', '', {})
                else:
                    calc += self.damage_calc(poke_type, move, opponent_type, ability[0], '', {})
            for t in opponent_type:
                calc -= self.damage_calc(opponent_type, Move(t=t, base_power=1.0), poke_type, poke_ability, '', {})
            if calc > potential:
                potential, pick = calc, p
        return pick
