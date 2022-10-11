from enum import Enum
from optparse import OptionParser

from bots.RandomBot import RandomBot
from bots.LittleTimmyBot import LittleTimmyBot
from bots.MinMaxBot import MinMaxBot
from bots.NeuralNetBot import NeuralNetBot


class BotOptions(Enum):
    RANDOM = 'random'
    JOEY = 'joey'
    MINMAX = 'minmax'
    DQN = 'dqn'


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-b', '--bot', dest='bot', choices=[b.value for b in BotOptions],
                      help='Bot options: [random, joey, minmax, dqn]. (Default=dqn)', default=BotOptions.DQN.value)
    options, _ = parser.parse_args()
    bot = {
        BotOptions.RANDOM.value: RandomBot(),
        BotOptions.JOEY.value: LittleTimmyBot(),
        BotOptions.MINMAX.value: MinMaxBot(),
        BotOptions.DQN.value: NeuralNetBot()
    }[options.bot]
    while True:
        bot.battle()
        bot.reset()
