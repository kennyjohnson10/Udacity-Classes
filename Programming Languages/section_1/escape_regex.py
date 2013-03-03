# Tricky REs with ^ and \

# Assign to regexp a regular expression for double-quoted string literals that
# allows for escaped double quotes.

# Hint: Escape " and \
# Hint: (?: (?: ) )

import re
import unittest

find_escaped_quote = '(?:\\\\\")'
find_two_escaped_quotes = '%s.+%s' % (find_escaped_quote, find_escaped_quote)
quotes_suround_find_two_escaped_quotes = '(?:\".*(?:%s).*\")' % find_two_escaped_quotes
regexp = quotes_suround_find_two_escaped_quotes

class TestEscapeRegex(unittest.TestCase):

	def test_find_escaped_quote(self):
		self.assertEqual(re.findall( r'%s' % find_escaped_quote,'"I say, \\""'), ['\\\"'])

	def test_find_two_escaped_quotes(self):
		self.assertEqual(re.findall( r'%s' % find_two_escaped_quotes,'\\"hello.\\"'), ['\\"hello.\\"'])

	def test_double_quoted_string_literal_with_escaped_quotes(self):
		self.assertEqual(re.findall(regexp,'"I say, \\"hello.\\""'), ['"I say, \\"hello.\\""'])

	def test_none_passing_string_literal(self):
		self.assertNotEqual(re.findall(regexp,'"\\"'), ['"\\"'])


