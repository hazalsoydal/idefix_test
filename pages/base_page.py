class BasePage:
    def __init__(self, driver):
        self.driver = driver

#every page needs a browser, instead of repeating we store it once.!!!other pages da reuse edicek

#burası iste driverı tutuyo boylelikle every other page can use it. shared toolbox gibi dusunebilirsin.


