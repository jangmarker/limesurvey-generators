import unittest

from ddt import ddt, data, unpack, file_data

import MultipleChoiceQuestionGenerator


@ddt
class MultipleChoiceQuestionGeneratorTest(unittest.TestCase):
    @file_data('multiplechoicequestions_expressions.json')
    @unpack
    def test_rating(self, name, correct, wrong, expression):
        self.assertEqual(MultipleChoiceQuestionGenerator.generate(name, correct, wrong), expression)
