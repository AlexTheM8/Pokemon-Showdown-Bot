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
    parser.add_option('-H', '--headless', dest='headless',
                      help='Enable this flag to run bot in headless mode.', action='store_true')
    options, _ = parser.parse_args()
    if options.bot == BotOptions.DQN.value:
        bot = NeuralNetBot(bool(options.headless))
    elif options.bot == BotOptions.RANDOM.value:
        bot = RandomBot(bool(options.headless))
    elif options.bot == BotOptions.JOEY.value:
        bot = YoungsterJoeyBot(bool(options.headless))
    else:
        bot = MinMaxBot(bool(options.headless))
    while True:
        bot.battle()
        bot.reset()
