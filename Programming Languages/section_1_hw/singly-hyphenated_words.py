# Singly-Hyphenated Words

# We examined hyphenated words in a quiz in class. In this problem you
# will get a chance to handle them correctly. 
# 
# Assign to the variable regexp a Python regular expression that matches 
# both words (with letters a-z) and also singly-hyphenated words. If you 
# use grouping, you must use (?: and ) as your regular expression
# parentheses. 
#
# Examples: 
#
# regexp exactly matches "astronomy"  
# regexp exactly matches "near-infrared"  
# regexp exactly matches "x-ray"  
# regexp does not exactly match "-tricky" 
# regexp does not exactly match "tricky-" 
# regexp does not exactly match "large - scale" 
# regexp does not exactly match "gamma-ray-burst" 
# regexp does not exactly match ""

# Your regular expression only needs to handle lowercase strings.

# In Python regular expressions, r"A|B" checks A first and then B - it 
# does not follow the maximal munch rule. Thus, you may want to check 
# for doubly-hyphenated words first and then non-hyphenated words.


import re
import unittest

regexp = r"(?:[a-z]+-[a-z]+)|[a-z]+" # you should replace this with your regular expression

# This problem includes an example test case to help you tell if you are on
# the right track. You may want to make your own additional tests as well.


class TestSinglyHyphenatedWords(unittest.TestCase):

	def test_input_of_single_word_string(self):
		result = re.findall(regexp, "astronomy")
		self.assertEqual(result, ['astronomy'])

	def test_input_of_single_word_with_hyphen(self):
		result = re.findall(regexp, "near-infrared")
		self.assertEqual(result, ['near-infrared'])

	def test_word_with_hyphen_before_word(self):
		result = re.findall(regexp, "-tricky")
		self.assertEqual(result, ['tricky'])

	def test_word_with_hyphen_after_word(self):
		result = re.findall(regexp, "tricky-")
		self.assertEqual(result, ['tricky'])

	def test_word_with_two_hyphens(self):
		result = re.findall(regexp, "gamma-ray-burst")
		self.assertEqual(result, ['gamma-ray', 'burst'])

	def test_words_with_hyphens_separated_by_spaces(self):
		result = re.findall(regexp, "gamma - ray - burst")
		self.assertEqual(result, ['gamma', 'ray', 'burst'])

	def test_single_letter_word(self):
		result = re.findall(regexp, "a")
		self.assertEqual(result, ['a'])

	def test_numbers_with_hyphens(self):
		result = re.findall(regexp, "1966-07-23")
		self.assertEqual(result, [])

test_case_input = """the wide-field infrared survey explorer is a nasa
infrared-wavelength space telescope in an earth-orbiting satellite which
performed an all-sky astronomical survey. be careful of -tricky tricky-
hyphens --- be precise."""

test_case_output = ['the', 'wide-field', 'infrared', 'survey', 'explorer',
'is', 'a', 'nasa', 'infrared-wavelength', 'space', 'telescope', 'in', 'an',
'earth-orbiting', 'satellite', 'which', 'performed', 'an', 'all-sky',
'astronomical', 'survey', 'be', 'careful', 'of', 'tricky', 'tricky',
'hyphens', 'be', 'precise']

if re.findall(regexp, test_case_input) == test_case_output:
	print "Test case passed."
else:
	print "Test case failed:" 
	print re.findall(regexp, test_case_input) 
