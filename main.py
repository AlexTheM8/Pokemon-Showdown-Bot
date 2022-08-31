from RandomBot import RandomBot
from driver import WebDriver

if __name__ == '__main__':
    driver = WebDriver()
    driver.run()
    # Run battle bot
    bot = RandomBot(driver)
    bot.battle()
