from bots.RandomBot import RandomBot
from bots.LittleTimmyBot import LittleTimmyBot

if __name__ == '__main__':
    # TODO Runtime args
    bot = LittleTimmyBot()
    while True:
        bot.battle()
        bot.reset()
