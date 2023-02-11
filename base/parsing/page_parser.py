from bs4 import BeautifulSoup
from base.data_fetching.web_driver import HeadlessWebDriver

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
}


class PageParser:
    def __init__(self, url: str):
        page_raw_data  = HeadlessWebDriver().get_raw_data_from_page(url)
        self.content = BeautifulSoup(page_raw_data, "html.parser")

    def get_elements(self, tag: str, class_: str):
        return self.content.find_all(tag, class_=class_)

    def get_element(self, tag: str, class_: str):
        return self.content.find(tag, class_=class_)
