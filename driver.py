from selenium import webdriver


class WebDriver:
    driver = webdriver.Edge()

    def __init__(self):
        self.driver.get('https://play.pokemonshowdown.com')
