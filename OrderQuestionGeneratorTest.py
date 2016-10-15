import unittest

from ddt import ddt, data, unpack, file_data

import OrderQuestionGenerator


@ddt
class OrderQuestionGeneratorTest(unittest.TestCase):
    @unpack
    @data(
        {'ref': 'abcd', 'actual': 'abcd', 'rating': 4},
        {'ref': 'abcd', 'actual': 'bcda', 'rating': 3},
        {'ref': 'abcd', 'actual': 'cdab', 'rating': 2},
        {'ref': 'abcd', 'actual': 'dcba', 'rating': 0},
        {'ref': 'abcd', 'actual': 'adcb', 'rating': 1},
        {'ref': 'abc', 'actual': 'cba', 'rating': 1},
        {'ref': ['alpha', 'beta'], 'actual': ['alpha', 'beta'], 'rating': 2},
    )
    def test_rating(self, ref, actual, rating):
        self.assertEqual(OrderQuestionGenerator.rate(ref, actual), rating)

    @data(
        ['ab', [(['a', 'b'], 2), (['b', 'a'], 0)]],
        [['alpha', 'beta'], [(['alpha', 'beta'], 2), (['beta', 'alpha'], 0)]],
        ['abc', [(['a', 'b', 'c'], 3), (['a', 'c', 'b'], 1), (['b', 'a', 'c'], 1), (['b', 'c', 'a'], 2), (['c', 'a', 'b'], 2), (['c', 'b', 'a'], 1)]]
    )
    @unpack
    def test_pairs(self, ref, results):
        self.assertListEqual(OrderQuestionGenerator.ratings(ref), results)

    # @skip("order of if clauses is arbitrary")
    @file_data('orderquestion_expressions.json')
    @unpack
    def test_expression(self, question, ref, expression):
        self.assertEqual(OrderQuestionGenerator.expression(question, ref), expression)
