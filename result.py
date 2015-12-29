import datetime


class Result(object):
    def __init__(self, score=0, timestamp=None, state=tuple()):
        self.timestamp = datetime.datetime.utcnow() if not timestamp else timestamp
        self.score = score
        self.state = state