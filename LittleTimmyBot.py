from random import randrange

from BattleBot import BattleBot
from BattleLogger import Move


class LittleTimmyBot(BattleBot):

    def choose_action(self):
        if self.active_fainted():
            self.choose_switch()
        else:
            options, has_z, mega_elem = self.move_options(modded=True)
            player_type, opponent_type = self.get_type(self.SELF_SIDE, num=1), self.get_type(self.OPPONENT_SIDE)
            ability = self.get_ability(self.OPPONENT_SIDE)
            stats = self.get_stats()
            strongest, pick = 0.0, options[randrange(len(options))][0]
            for v, m in options:
                if len(ability) > 1:
                    calc = self.damage_calc(player_type, m, opponent_type, '', stats)
                else:
                    calc = self.damage_calc(player_type, m, opponent_type, ability[0], stats)
                if calc > strongest:
                    strongest, pick = calc, v
            self.choose_move(pick, has_z, mega_elem)

    def best_pick(self):
        party = self.party_options()
        opponent_type = self.get_type(self.OPPONENT_SIDE)
        ability = self.get_ability(self.OPPONENT_SIDE)
        potential, pick = -10, party[randrange(len(party))]
        for i, p in enumerate(party):
            poke_type = self.get_type(self.SELF_SIDE, int(p))
            poke_ability = self.get_ability(self.SELF_SIDE, num=p)
            calc = 0.0
            for t in poke_type:
                move = Move(t=t, base_power=1.0)
                if len(ability) > 1:
                    calc += self.damage_calc(poke_type, move, opponent_type, '', {})
                else:
                    calc += self.damage_calc(poke_type, move, opponent_type, ability[0], {})
            for t in opponent_type:
                calc -= self.damage_calc(opponent_type, Move(t=t, base_power=1.0), poke_type, poke_ability, {})
            if calc > potential:
                potential, pick = calc, p
        return pick
