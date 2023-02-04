import re

from parsing.page_parser import PageParser


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
            "score":           self.content.select_one('[aria-label="Downvote"]').find_previous().text.replace("•", "0"),
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

    def get_comments_and_replies(self):
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
