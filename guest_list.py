from collections import namedtuple, defaultdict


class Guest(namedtuple('Guest', ['name'])):
	def __repr__(self):
		return str(self.name)


class GuestList(object):
	_INPUT_GRID_START_ROW = 2
	_INPUT_GRID_START_COL = 0
	_NAME_COLUMN_INDEX = 1

	# So you can exclude people from the table seating (e.g. top table)
	_INCLUDE_IN_TABLES_ROW = 0

	def __init__(self, guest_list_file):
		"""
        Read the bottom triangle of the grid. Ignore the top half
        """
		self._guests = dict()
		self._relationships = defaultdict(lambda: 0)
		input_grid = [l.split(',') for l in open(guest_list_file)]
		all_names = [n.strip() for n in input_grid[self._INPUT_GRID_START_ROW] if n]
		guest_names_to_seat = set()
		for i in range(len(all_names)):
			row_index = i + 1 + self._INPUT_GRID_START_ROW
			row = input_grid[row_index]
			guest_name = row[self._NAME_COLUMN_INDEX].strip()
			assert all_names[i].strip() == guest_name
			if not int(row[self._INCLUDE_IN_TABLES_ROW]):
				continue
			self._guests[guest_name] = Guest(name=guest_name)
			for j in range(i):
				col_index = j + self._NAME_COLUMN_INDEX + 1
				weight = input_grid[row_index][col_index]
				other_guest_name = all_names[j]
				if weight and other_guest_name in self._guests:
					pair = frozenset([self._guests[guest_name], self._guests[other_guest_name]])
					assert pair not in self._relationships
					self._relationships[pair] = int(weight)

	def __len__(self):
		return len(self._guests)

	def relationship_weight(self, person_one, person_two):
		return self._relationships[frozenset([person_one, person_two])]

	def relationships(self):
		return self._relationships

	def guests(self):
		return list(self._guests.values())

	def guest(self, name):
		return self._guests.get(name)
