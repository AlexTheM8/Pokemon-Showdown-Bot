import BattleBot


class RandomBot(BattleBot.BattleBot):

    def battle(self):
        self.read_team(BattleBot.SELF_SIDE)
        # while self.in_battle:
        #     # Read both sides
        #     self.read_team(BattleBot.SELF_SIDE)
        #     self.read_team(BattleBot.OPPONENT_SIDE)

    def choose_action(self):
        pass
