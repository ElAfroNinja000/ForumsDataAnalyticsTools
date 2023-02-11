import re

from base.parsing.page_parser import PageParser
from reddit.reddit_parsing.reddit_comment_parser import RedditCommentParser


class RedditPostParser(PageParser):
    def __init__(self, url: str):
        self.url = url
        super().__init__(self.url)

    def get_post_data(self):
        return {
            "score":           self.content.select_one('[aria-label="Downvote"]').find_previous().text.replace("•", "0"),
            "title":           self.content.select_one('[data-adclicklocation="title"]').select_one("h1").text,
            "timestamp":       self.content.select_one('[data-testid="post_timestamp"]').text,
            "comments_count":  self.content.select_one('[data-click-id="comments"]').select_one("span").text.split(" ")[0]
        }

    def get_community_data(self):
        return {
            "title":              self.content.select_one('[data-redditstyle="false"]').select_one("span").text,
            "creation_date":      self.content.find(id=re.compile(r"^IdCard--CakeDay--undefined.*?$")).select_one("span").text,
            "members_count":      self.content.find(id=re.compile(r"^IdCard--Subscribers--undefined.*?$")).find_previous().text
        }

    def get_comments(self):
        comment_section = self.content.find('div', attrs={'data-scroller-first': True}).find_previous() \
                                      .find_all("div", attrs={'id': True, "style": True, "tabindex": True})
        comments = [RedditCommentParser(comment) for comment in comment_section
                    if comment.find(class_=re.compile(r"^Comment .*?$"))]
        return [comment for comment in comments if comment.is_available()]

    def get_comments_and_replies(self, topic: str, post: str):
        comments = self.get_comments()
        comments_depths = [comment.get_data(topic, post)["depth"] for comment in comments]

        stack = []
        replies_per_comment = [[] for _ in comments]
        for i, comment_depth in enumerate(comments_depths):
            while stack and comments_depths[stack[-1]] >= comment_depth:
                stack.pop()
            if stack:
                replies_per_comment[stack[-1]].append(comments[i])
            stack.append(i)
        return list(zip(comments, replies_per_comment))

    def make_post_data(self, topic: str):
        post_data      = self.get_post_data()
        community_data = self.get_community_data()
        return {
            "topic":          topic,
            "post_data":      post_data,
            "community_data": community_data
        }
