from parsing.page_parser import PageParser


class RedditRequestParser(PageParser):
    def __init__(self, base_url: str, base_request: str):
        self.base_url = base_url
        self.base_request = base_request
        self.request_url = self.make_request_url(base_url, base_request)
        super().__init__(self.request_url)

    @staticmethod
    def make_request_url(base_url: str, request: str):
        request = request.replace(" ", "%20")
        return f"{base_url}/search/?q={request}"

    def get_posts_urls(self):
        posts_list   = self.content.select_one('[data-testid="posts-list"]')
        posts_titles = posts_list.select('[data-adclicklocation=title]')

        return [f'{self.base_url}{post_title.select_one("a").get("href")}'
                for post_title in posts_titles]
