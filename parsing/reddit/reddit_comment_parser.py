class RedditCommentParser:
    def __init__(self, comment):
        self.comment = comment

    def get_data(self):
        available_text = self.comment.select_one('[data-testid="comment"]')
        text = available_text.select_one("p").text if available_text else ""
        available_score = self.comment.select_one('[aria-label="Downvote"]')
        score = available_score.find_previous().text.replace("•", "0") if available_score else "0"
        return {
            "depth":     int(self.comment.select_one('[data-testid="post-comment-header"]').find_previous().text.split(" ")[-1]),
            "timestamp": self.comment.select_one('[data-testid="comment_timestamp"]').text,
            "text":      text,
            "score":     score
        }

