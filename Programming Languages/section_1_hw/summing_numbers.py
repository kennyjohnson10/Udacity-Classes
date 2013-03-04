# Title: Summing Numbers

# Write a procedure called sumnums(). Your procedure must accept as input a
# single string. Your procedure must output an integer equal to the sum of
# all integer numbers (one or more digits in sequence) within that string.
# If there are no decimal numbers in the input string, your procedure must
# return the integer 0. The input string will not contain any negative integers.
#
# Example Input: "hello 2 all of you 44"
# Example Output: 46
#
# Hint: int("44") == 44

import re
import unittest

def sumnums(sentence): 
	# write your code here
	result = 0

	regex = r'\d+' # or r'[0-9]+'
	arr_result = re.findall(regex, sentence)

	if len(arr_result) == 0:
		return result
	else:
		for number in arr_result:
			result += int(number)
		return result


class TestSummingNumbers(unittest.TestCase):

	def test_input_of_single_string(self):
		result = sumnums('34')
		self.assertEqual(int, type(result))

	def test_input_of_string_with_no_integer_values(self):
		result = sumnums('abc')
		self.assertEqual(0, result)
	
	def test_correct_addition_of_ints_in_input(self):
		result = sumnums('abc 23, 5')
		self.assertEqual(28, result)
		 

# This problem includes an example test case to help you tell if you are on
# the right track. You may want to make your own additional tests as well.

test_case_input = """The Act of Independence of Lithuania was signed 
on February 16, 1918, by 20 council members."""

test_case_output = 1954

if sumnums(test_case_input) == test_case_output:
  print "Test case passed."
else:
  print "Test case failed:" 
  print sumnums(test_case_input) 




