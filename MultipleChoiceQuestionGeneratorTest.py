import unittest

from ddt import ddt, data, unpack, file_data

import MultipleChoiceQuestionGenerator


@ddt
class MultipleChoiceQuestionGeneratorTest(unittest.TestCase):
    @unpack
    @data(
        {'name': 'multiple', 'correct': ['sha', 'bei'], 'wrong': ['ber', 'fra'],
         'expression': "{max(0, sum(if(multiple_sha == 'Y', 1, 0), if(multiple_bei == 'Y', 1, 0), if(multiple_ber == 'Y', -1, 0), if(multiple_fra == 'Y', -1, 0))}"
         },
    )
    def test_rating(self, name, correct, wrong, expression):
        self.assertEqual(MultipleChoiceQuestionGenerator.generate(name, correct, wrong), expression)
