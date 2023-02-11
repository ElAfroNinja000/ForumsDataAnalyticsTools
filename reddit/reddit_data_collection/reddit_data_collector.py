import os

from reddit.reddit_parsing.reddit_request_parser import RedditRequestParser
from reddit.reddit_parsing.reddit_post_parser import RedditPostParser


class RedditDataCollector:
    def __init__(self, url: str, requests: list):
        self.url     = url
        self.requests = requests

    def run(self, limit: int):
        posts    = []
        comments = []

        for request in self.requests:
            request_parser = RedditRequestParser(self.url, request)
            posts_urls = request_parser.get_posts_urls()

            for i, post_url in enumerate(posts_urls):
                if i >= limit != 0:
                    break
                post_parser = RedditPostParser(post_url)
                post = post_parser.make_post_data(request)
                post_comments = post_parser.get_comments_and_replies(request, post["post_data"]["title"])
                for comment in post_comments:
                    replies = []
                    for reply in comment[1]:
                        replies.append(reply.get_data(request, post["post_data"]["title"]))
                    comment = {
                        "comment_data": comment[0].get_data(request, post["post_data"]["title"]),
                        "replies":      replies
                    }
                    comments.append(comment)
                posts.append(post)
        return posts, comments
