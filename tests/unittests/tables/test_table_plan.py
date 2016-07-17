from unittest import TestCase

from guest_list import Guest
from tables.table import Table
from tables.table_plan import pick_exactly_n_from_table, get_tens


class TestThings(TestCase):
	def test_get_tens(self):
		relationships = {
			frozenset(['a', 'b']): 10,
			frozenset(['b', 'c']): 10,

		}
		people = ['a', 'b', 'c']
		the_one = 'a'
		self.assertEqual(get_tens(people, relationships, the_one), {'a', 'b', 'c'})
