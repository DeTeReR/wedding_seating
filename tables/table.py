import copy

import itertools
from collections import defaultdict

from tables.score import Score


class TableException(Exception):
	pass


class PrettyPrintSet(set):
	def __repr__(self):
		return '{%s}' % ', '.join(sorted(repr(x) for x in self))


class Table(object):
	def __init__(self, max_size):
		self._seat_count = max_size
		self._guests = PrettyPrintSet()

	def __str__(self):
		return 'Table(_max_size=%s, _guests=%s)' % (self._seat_count, self._guests)

	def add_guests(self, guests):
		for guest in guests:
			self.add_guest(guest)

	def remove_guests(self, guests):
		for guest in guests:
			self.remove_guest(guest)

	def add_guest(self, guest):
		if guest in self._guests:
			raise TableException('%s is already on this table!', guest.name)
		if len(self._guests) >= self._seat_count:
			raise TableException('Too many guests on this table, can\'t add %s.', guest.name)
		self._guests.add(guest)

	def remove_guest(self, guest):
		if guest not in self._guests:
			raise TableException('Can\'t remove %s from table, they aren\'t sitting here.', guest.name)
		self._guests.remove(guest)

	def guests(self):
		return self._guests

	def state(self):
		return copy.copy(self._guests)

	def seat_count(self):
		return self._seat_count

	def score(self, relationships):
		table_score = 0
		person_scores = defaultdict(int)
		for pair_of_people in itertools.combinations(self.guests(), 2):
			pair_score = relationships[frozenset(pair_of_people)]
			for person in pair_of_people:
				person_scores[person] += pair_score
			table_score += pair_score

		lowest_person_score = min(person_scores.values()) if person_scores else None
		return Score(
			total=table_score,
			lowest_table_score=table_score,
			lowest_person_score=lowest_person_score
		)