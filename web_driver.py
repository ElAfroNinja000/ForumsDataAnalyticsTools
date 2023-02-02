from selenium import webdriver

OPTIONS = ["--disable-extensions", "--disable-gpu", "--no-sandbox", "start-maximized", "disable-infobars",
           "--disable-dev-shm-usage", "--disable-browser-side-navigation", "--disable-gpu-sandbox", "--headless"]


class HeadlessWebDriver:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.headless = True
        for option in OPTIONS:
            self.options.add_argument(option)
        self.driver = webdriver.Chrome(options=self.options, executable_path=r"D:\Python\Lib\site-packages\chromedriver_win32\chromedriver.exe")

    def get_raw_data_from_page(self, url):
        self.driver.get(url)
        html = self.driver.page_source
        self.driver.quit()
        return html

