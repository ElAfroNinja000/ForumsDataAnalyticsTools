class RedditCommentParser:
    def __init__(self, comment):
        self.available = "SignalementSauvegarderSuivre" in comment.text
        if self.available:
            self.depth     = int(comment.select_one('[data-testid="post-comment-header"]').find_previous().text.split(" ")[-1])
            self.timestamp = comment.select_one('[data-testid="comment_timestamp"]').text.replace("il y a ", "")
            self.text      = comment.select_one('[data-testid="comment"]').select_one("p").text
            self.score     = int(comment.select_one('[aria-label="Downvote"]').find_previous().text.replace("•", "0"))
        else:
            self.depth     = 1
            self.timestamp = ""
            self.text      = ""
            self.score     = 0

    def is_available(self):
        return self.available

    def get_data(self, topic: str, post: str):
        return {
            "topic":     topic,
            "post":      post,
            "depth":     self.depth,
            "timestamp": self.timestamp,
            "text":      self.text,
            "score":     self.score
        }

