from guests.relationship import Relationship


class Guest(object):
    def __init__(self, name, sex):
        self._name = name
        self.sex = sex
        self._relationships = set()

    def add_relationship(self, relationship):
        self._relationships.add(relationship)
