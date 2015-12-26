class Relationship(object):
    def __init__(self, person, other_person, weight):
        self.weight = weight
        self._people = frozenset([person, other_person])

    def __contains__(self, person):
        return bool(person in self._people)