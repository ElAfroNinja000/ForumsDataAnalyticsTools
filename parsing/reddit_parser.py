import re

from parsing.page_parser import PageParser


BASE_URL = "https://www.reddit.com"


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


class RedditPostParser(PageParser):
    def __init__(self, url: str):
        self.url = url
        super().__init__(self.url)

    def get_data(self):
        community_info = {
            "title":              self.content.select_one('[data-redditstyle="false"]').select_one("span").text,
            "creation_date":      self.content.find(id=re.compile(r"^IdCard--CakeDay--undefined.*?$")).select_one("span").text,
            "members_count":      self.content.find(id=re.compile(r"^IdCard--Subscribers--undefined.*?$")).find_previous().text
        }
        return {
            "score":           int(self.content.select_one('[aria-label="Downvote"]').find_previous().text.replace("•", "0")),
            "title":           self.content.select_one('[data-adclicklocation="title"]').select_one("h1").text,
            "timestamp":       self.content.select_one('[data-testid="post_timestamp"]').text,
            "comments_count":  int(self.content.select_one('[data-click-id="comments"]').select_one("span").text.split(" ")[0]),
            "community_info":  community_info
        }

    def get_comments(self):
        comment_section = self.content.find('div', attrs={'data-scroller-first': True}).find_previous() \
                                      .find_all("div", attrs={'id': True, "style": True, "tabindex": True})
        return [comment for comment in comment_section
             if comment.find(class_=re.compile(r"^Comment .*?$"))]

    def get_comments_replies(self):
        comments = self.get_comments()
        comments_depths = [int(comment.select_one('[data-testid="post-comment-header"]').find_previous().text.split(" ")[-1])
                           for comment in comments]

        replies_per_comment = []
        for i, comment_depth in enumerate(comments_depths):
            comment_replies = []
            for j, next_comment_depth in enumerate(comments_depths[i + 1:]):
                if next_comment_depth > comment_depth:
                    comment_replies.append(comments[i + j + 1])
                else:
                    break
            replies_per_comment.append(comment_replies)
        return list(zip(comments, replies_per_comment))


class RedditCommentParser:
    def __init__(self, comment, replies):
        self.comment = comment
        self.replies = replies

    def get_data(self):
        return {
            "depth":     int(self.comment.select_one('[data-testid="post-comment-header"]').find_previous().text.split(" ")[-1]),
            "timestamp": self.comment.select_one('[data-testid="comment_timestamp"]').text,
            "text":      self.comment.select_one('[data-testid="comment"]').select_one("p").text,
            "score":     int(self.comment.select_one('[aria-label="Downvote"]').find_previous().text.replace("•", "0"))
        }


if __name__ == "__main__":
    # Request Parser Test
    parser = RedditRequestParser(BASE_URL, "Venezuala food")
    posts = parser.get_posts_urls()
    print(posts)

    # Post Parser Test
    # post_parser = RedditPostParser("https://www.reddit.com/r/france/comments/10sqie6/que_faire_avec_mes_vieux_voisins/")
    # comments = post_parser.get_comments_replies()
    # print(post_parser.get_data())

    # Comment Parser Test
    # comment, replies = comments[10]
    # comment_parser = RedditCommentParser(comment, replies)
    # print(comment_parser.get_data())
