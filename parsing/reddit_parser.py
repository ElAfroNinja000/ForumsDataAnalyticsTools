from parsing.page_parser import PageParser


BASE_URL = "https://www.reddit.com"


class RedditRequestParser(PageParser):
    def __init__(self, base_url: str, base_request: str):
        self.request_url = self.make_request_url(base_url, base_request)
        super().__init__(self.request_url)
        self.base_url      = base_url
        self.base_request  = base_request
        self.posts_urls    = self.get_posts_urls()

    @staticmethod
    def make_request_url(base_url: str, request: str):
        request = request.replace(" ", "%20")
        return f"{base_url}/search/?q={request}"

    def get_posts_urls(self):
        posts_list   = self.page_html_data.select_one('[data-testid="posts-list"]')
        posts_titles = posts_list.select('[data-adclicklocation=title]')

        return [f'{self.base_url}{post_title.select("a")[0].get("href")}'
                for post_title in posts_titles]


class RedditPostParser(PageParser):
    def __init__(self, url: str):
        self.url = url
        super().__init__(self.url)

    def get_post_info(self):
        return

    def get_comments(self):
        return

    def get_comment_data(self):
        return


if __name__ == "__main__":
    parser = RedditRequestParser(BASE_URL, "Donkey Kong")
    posts = parser.get_posts()
    print()
