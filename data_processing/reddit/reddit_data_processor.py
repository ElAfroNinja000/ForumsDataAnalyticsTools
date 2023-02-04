import os
import json

from parsing.reddit.reddit_request_parser import RedditRequestParser
from parsing.reddit.reddit_post_parser    import RedditPostParser
from parsing.reddit.reddit_comment_parser import RedditCommentParser

BASE_URL = "https://www.reddit.com"
NUMBER_OF_POSTS = 1


class RedditDataProcessor:
    def __init__(self, url: str, request: str):
        self.url     = url
        self.request = request

    @staticmethod
    def make_post_data(post_parser: RedditPostParser):
        post_data = post_parser.get_data()
        post_comments = post_parser.get_comments_and_replies()
        return {
            "post_data":     post_data,
            "post_comments": post_comments
        }

    def run(self, limit: int):
        request_parser = RedditRequestParser(self.url, self.request)
        posts_urls = request_parser.get_posts_urls()

        posts = []
        for i, post_url in enumerate(posts_urls):
            post_parser = RedditPostParser(post_url)
            post = self.make_post_data(post_parser)
            comments = []
            for comment in post["post_comments"]:
                comment_data = RedditCommentParser(comment[0]).get_data()
                replies = []
                for reply in comment[1]:
                    reply_data = RedditCommentParser(reply).get_data()
                    replies.append(reply_data)
                comment = {
                    "comment_data": comment_data,
                    "replies":      replies
                }
                comments.append(comment)
            post["comments"] = comments
            posts.append(post)
            if i >= limit != 0:
                break
        return posts


if __name__ == "__main__":
    reddit_data_processor = RedditDataProcessor(BASE_URL, "fried chicken")

    with open(f"{os.getcwd()}/data/test.json", "w") as file:
        file.write(json.dumps(reddit_data_processor.run(NUMBER_OF_POSTS)))
