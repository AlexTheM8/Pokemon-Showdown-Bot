from bots.BattleBot import BattleBot

# TODO
'''
Sort data into winning & losing
Log init conditions & action taken
Bot will train on that data, then given init conditions & action, predict whether in win/lose
OR do reinforcement learning
Reward eq = PHC - OHC + PSC - OSC - PS + OS
P/OHC = Player/Opponent Health Change (100, -100)
P/OSC = Player/Opponent Stat Change (30, -30) 1 point per stat (max 6 per stat)
P/OS = Player/Opponent Status (10, -10) Whether gaining/losing a status condition
Equation range: (280, -280)
'''


class NeuralNetBot(BattleBot):

    def choose_action(self):
        pass

    def best_pick(self):
        pass

    def __repr__(self):
        return 'NeuralNetBot'
