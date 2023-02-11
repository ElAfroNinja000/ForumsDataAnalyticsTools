import pandas as pd

from reddit.reddit_data_collection.reddit_data_collector import RedditDataCollector


BASE_URL = "https://www.reddit.com"


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

    def get_most_popular_comment(self, topic: str, index: int):
        return self.comments.loc[self.comments["score"] == self.comments["score"].max()]

    @staticmethod
    def __get_flattened_comments__(comments: list):
        flattened_comments = []
        for comment in comments:
            flattened_comments.append(comment["comment_data"])
            flattened_comments = flattened_comments + comment["replies"]
        return flattened_comments


if __name__ == "__main__":
    reddit_data_analyzer = RedditDataAnalyzer()
    reddit_data_analyzer.get_data(["food trucks"], 1)
    print(reddit_data_analyzer.posts.head())
    print(reddit_data_analyzer.comments.head())

