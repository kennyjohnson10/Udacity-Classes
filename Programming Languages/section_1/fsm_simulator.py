# FSM Simulation
import unittest

edges = {(1, 'a') : 2,
		 (2, 'a') : 2,
		 (2, '1') : 3,
		 (3, '1') : 3}

accepting = [3]

def fsmsim(string, current, edges, accepting):
	'''
	(str, int, dict, array) --> bool
	>>> print fsmsim("aaa111",1,edges,accepting)
	True
	'''
	if string == "":
		return current in accepting
	else:
		letter = string[0]

		# Is there a valid edge?
		try:
			current = edges[(current, letter)]

			# If so, take it.
			if len(string) > 1:
				return fsmsim(string[1:], current, edges, accepting)
			else:
				return fsmsim("", current, edges, accepting)

		# If not, return False.
		except KeyError:
			return False


class TestFSMSim(unittest.TestCase):

	def test_false_input_for_fsm(self):
		self.assertFalse(fsmsim("3",1,edges,accepting))

	def test_true_input_for_fsm(self):
		self.assertTrue(fsmsim("aa1",1,edges,accepting))