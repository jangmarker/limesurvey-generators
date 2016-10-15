import unittest

from ddt import ddt, data, unpack, file_data

import MultipleChoiceQuestionGenerator


@ddt
class MultipleChoiceQuestionGeneratorTest(unittest.TestCase):
    @file_data('multiplechoicequestion_expressions.json')
    @unpack
    def test_rating(self, question, correct, wrong, expression):
        self.assertEqual(MultipleChoiceQuestionGenerator.generate(question, correct, wrong), expression)
