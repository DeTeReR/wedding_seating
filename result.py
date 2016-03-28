import datetime

from tables.score import Score


class Result(object):
    def __init__(self, score=None, timestamp=None, state=tuple()):
        score = Score() if score is None else score
        self.timestamp = datetime.datetime.utcnow() if not timestamp else timestamp
        self.score = score
        self.state = state
