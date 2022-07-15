import random

from ..cards.models import ProbabilityTest


def test_probability_calculator():
    def test_func():
        return True

    assert 100 == ProbabilityTest.run_probability_test(test_func, 2)

    def test_func():
        return False

    assert 0 == ProbabilityTest.run_probability_test(test_func, 2)

    def test_func():
        return random.choice([1, 2]) == 2

    # Out of 100 runs, it is nearly certain that probability of 50% will occur
    # more than 20 and less than 80 times
    assert 20 < ProbabilityTest.run_probability_test(test_func, 100) < 80


def test_probability_calculator_with_arguments():
    def test_func(argument):
        return argument

    assert 100 == ProbabilityTest.run_probability_test(test_func, 2, argument=True)

    def test_func(argument):
        return argument

    assert 0 == ProbabilityTest.run_probability_test(test_func, 2, argument=False)
