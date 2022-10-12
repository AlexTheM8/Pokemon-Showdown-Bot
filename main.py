from enum import Enum
from optparse import OptionParser

from bots.RandomBot import RandomBot
from bots.YoungsterJoeyBot import YoungsterJoeyBot
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
    if options.bot == BotOptions.DQN.value:
        bot = NeuralNetBot()
    elif options.bot == BotOptions.RANDOM.value:
        bot = RandomBot()
    elif options.bot == BotOptions.JOEY.value:
        bot = YoungsterJoeyBot()
    else:
        bot = MinMaxBot()
    while True:
        bot.battle()
        bot.reset()
