from BattleBot import BattleBot


class RandomBot(BattleBot):

    def battle(self):
        self.read_team(BattleBot.SELF_SIDE)
        self.battle_logger.save_data()
        # while self.in_battle:
        #     # Read both sides
        #     self.read_team(BattleBot.SELF_SIDE)
        #     self.read_team(BattleBot.OPPONENT_SIDE)

    def choose_action(self):
        pass
