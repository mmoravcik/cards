import pytest
import random

from ..cards import StandardDeck, JokerDeck, Card

from ..cards import constants
from ..cards import exceptions


def test_probability_calculator():
    def test_func():
        return True

    assert 100 == StandardDeck.run_probability_test(test_func, 5)

    def test_func():
        return False

    assert 0 == StandardDeck.run_probability_test(test_func, 5)

    def test_func():
        return random.choice([1, 2]) == 2

    # Out of 100 runs, it is nearly certain that probability of 50% will occur
    # more than 20 and less than 80 times
    assert 20 < StandardDeck.run_probability_test(test_func, 100) < 80


def test_probability_calculator_with_arguments():
    def test_func(argument):
        return argument

    assert 100 == StandardDeck.run_probability_test(test_func, 5, argument=True)

    def test_func(argument):
        return argument

    assert 0 == StandardDeck.run_probability_test(test_func, 5, argument=False)
