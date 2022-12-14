from random import randrange

from bots.BattleBot import BattleBot


class RandomBot(BattleBot):

    def choose_action(self):
        if self.active_fainted():
            self.choose_switch()
        else:
            # Limit to moves only if cannot switch
            party = self.party_options()
            if randrange(1, 6) < 5 or not party:
                options, has_z, mega_elem = self.move_options()
                self.choose_move(options[randrange(len(options))][0], has_z, mega_elem)
            else:
                self.choose_switch()

    def best_pick(self):
        party = self.party_options()
        return party[randrange(len(party))]

    def __repr__(self):
        return 'RandomBot'
