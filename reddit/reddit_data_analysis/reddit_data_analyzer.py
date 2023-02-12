import pandas as pd
from collections import Counter

from reddit.reddit_data_collection.reddit_data_collector import RedditDataCollector


BASE_URL = "https://www.reddit.com"
EXCLUDED_WORDS = ["the", "and", "a", "of", "is", "to", "it", "that", "in", "are",
                  "for", "he", "have", "I", "this", "at", "just", "not", "The", "you"]


class RedditDataAnalyzer:
    def __init__(self):
        self.posts    = {}
        self.comments = {}

    def get_data(self, topics: list, number_of_posts: int):
        reddit_data_collector = RedditDataCollector(BASE_URL, topics)
        posts, comments = reddit_data_collector.run(number_of_posts)

        posts_data = [post["post_data"] for post in posts]
        self.posts = pd.DataFrame(posts_data)

        comments = self.__get_flattened_comments__(comments)
        df_comments = pd.json_normalize(comments)
        df_comments = df_comments.reset_index(drop=True)
        self.comments = df_comments

    def get_most_popular_comment(self, topic: str = None):
        if topic:
            return self.comments.loc[(self.comments["score"] == self.comments["score"].max())
                                   & (self.comments["topic"] == topic)].reset_index(drop=True)

        return self.comments.loc[self.comments["score"] == self.comments["score"].max()].reset_index(drop=True)

    def get_most_popular_post(self, with_comments: bool = False):
        if with_comments:
            grouped = self.comments.groupby("post")["score"].sum().reset_index()
            grouped["total"] = (grouped["score"] + self.posts["score"]) / 2
            return grouped.loc[grouped["score"] == grouped["score"].max()].reset_index(drop=True)

        return self.posts.loc[self.posts["score"] == self.posts["score"].max()].reset_index(drop=True)

    def get_most_frequent_words(self, count: int, topic: str = None):
        if topic:
            data = self.comments.loc[self.comments["topic"] == topic].reset_index(drop=True)
        else:
            data = data = self.comments
        data["words"] = data["text"].str.split()
        df_words = data.explode("words")
        df_words = df_words[~df_words['words'].isin(EXCLUDED_WORDS)]
        word_counts = df_words["words"].value_counts()
        return word_counts.head(count)

    @staticmethod
    def __get_flattened_comments__(comments: list):
        flattened_comments = []
        for comment in comments:
            flattened_comments.append(comment["comment_data"])
            flattened_comments = flattened_comments + comment["replies"]
        return flattened_comments


if __name__ == "__main__":
    reddit_data_analyzer = RedditDataAnalyzer()
    reddit_data_analyzer.get_data(["ancient greece"], 5)

    # print(reddit_data_analyzer.get_most_popular_comment("ancient greece"))
    # print(reddit_data_analyzer.get_most_popular_post(with_comments=True))
    print(reddit_data_analyzer.get_most_frequent_words(20, "ancient greece"))
