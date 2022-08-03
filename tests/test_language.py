import pytest

from ..cards.constants import (
    SUIT_HEARTS,
    SUIT_DIAMONDS,
    COLOUR_RED,
    SUIT_CLUBS,
    COLOUR_BLACK,
)
from ..cards.language import Language
from ..cards.models import ProbabilityTest

ITERATION_COUNT = 15000

pytestmark = pytest.mark.skip("These are tests of the old language")


def test_red_card_probability():
    red_card_probability = [
        {"action": "start_with", "command": "standard_deck"},
        {"action": "pick", "command": "random_cards", "meta": {"count": 1}},
        {
            "action": "compare_picked",
            "command": "any_match",
            "meta": {
                "conditions": [
                    {
                        "type": "colours",
                        "values": [COLOUR_RED],
                    }
                ],
                "from_sequence": 2,
            },
        },
    ]

    lan = Language(sequences=red_card_probability)
    result = ProbabilityTest.run_language_probability_test(
        lan.execute,
        iteration_count=ITERATION_COUNT,
        result_sequence=3,
    )
    assert 49 < result < 51
    print("Chance of a red card is {}%".format(result))


def test_high_card_probability():
    """
    Probability of one of the picked card being AKQJ or 10
    """
    high_card_probability = [
        {"action": "start_with", "command": "standard_deck"},
        {"action": "pick", "command": "random_cards", "meta": {"count": 5}},
        {
            "action": "compare_picked",
            "command": "any_match",
            "meta": {
                "conditions": [
                    {
                        "type": "values",
                        "values": [1, 13, 12, 11, 10],
                    }  # Ace is 1
                ],
                "matches_required": 1,
            },
        },
    ]

    lan = Language(sequences=high_card_probability)
    result = ProbabilityTest.run_language_probability_test(
        lan.execute, iteration_count=ITERATION_COUNT, result_sequence=3
    )
    assert 91 < result < 93
    print("Chance of a high card is {}%".format(result))


def test_cutting_a_joker_probability():
    """
    Probability of cutting a joker in a game of "joker"
    """
    cutting_a_joker_probability = [
        {"action": "start_with", "command": "canasta_deck"},
        {"action": "pick", "command": "random_cards", "meta": {"count": 3}},
        {
            "action": "compare_picked",
            "command": "any_match",
            "meta": {
                "conditions": [
                    {
                        "type": "values",
                        "values": ["*"],
                    }
                ],  # joker
                "matches_required": 1,
            },
        },
    ]

    lan = Language(sequences=cutting_a_joker_probability)
    result = ProbabilityTest.run_language_probability_test(
        lan.execute, iteration_count=ITERATION_COUNT, result_sequence=3
    )
    assert 10 < result < 12
    print("Chance of cutting a joker is {}%".format(result))

    # Now lets try 2 joker probability
    cutting_two_jokers_probability = cutting_a_joker_probability
    cutting_two_jokers_probability[2]["meta"]["matches_required"] = 2

    lan = Language(sequences=cutting_two_jokers_probability)
    result = ProbabilityTest.run_language_probability_test(
        lan.execute, iteration_count=ITERATION_COUNT, result_sequence=3
    )
    assert 0 < result < 0.8
    print("Chance of cutting two jokers is {}%".format(result))


def test_picking_a_single_specific_card():
    picking_a_single_specific_card = [
        {"action": "start_with", "command": "standard_deck"},
        {"action": "pick", "command": "random_cards", "meta": {"count": 1}},
        {
            "action": "compare_picked",
            "command": "any_match",
            "meta": {
                "conditions": [
                    {
                        "type": "specific_cards",
                        "values": [{"value": 1, "suit": SUIT_HEARTS}],
                    }
                ],
                "matches_required": 1,
            },
        },
    ]

    lan = Language(sequences=picking_a_single_specific_card)
    result = ProbabilityTest.run_language_probability_test(
        lan.execute, iteration_count=ITERATION_COUNT, result_sequence=3
    )
    assert 1.6 < result < 2.5
    print("Chance of picking an ace of hearths is {}%".format(result))


def test_picking_specific_2_cards_out_of_26_picked():
    picking_specific_2_cards_out_of_26_picked = [
        {"action": "start_with", "command": "standard_deck"},
        {"action": "pick", "command": "random_cards", "meta": {"count": 26}},
        {
            "action": "compare_picked",
            "command": "any_match",
            "meta": {
                "conditions": [
                    {
                        "type": "specific_cards",
                        "values": [
                            {"value": 1, "suit": SUIT_HEARTS},
                            {"value": 2, "suit": SUIT_HEARTS},
                        ],
                    }
                ],
                "matches_required": 2,
            },
        },
    ]

    lan = Language(sequences=picking_specific_2_cards_out_of_26_picked)
    result = ProbabilityTest.run_language_probability_test(
        lan.execute, iteration_count=ITERATION_COUNT, result_sequence=3
    )
    assert 23 < result < 25.5
    print("Chance of picking specific 2 cards out of 26 is {}%".format(result))


def test_picking_3_cards_no_spade():
    picking_3_cards_no_spade = [
        {"action": "start_with", "command": "standard_deck"},
        {"action": "pick", "command": "random_cards", "meta": {"count": 3}},
        {
            "action": "compare_picked",
            "command": "any_match",
            "meta": {
                "conditions": [
                    {
                        "type": "suits",
                        "values": [SUIT_HEARTS, SUIT_DIAMONDS, SUIT_CLUBS],
                    }
                ],
                "matches_required": 3,
            },
        },
    ]

    lan = Language(sequences=picking_3_cards_no_spade)
    result = ProbabilityTest.run_language_probability_test(
        lan.execute, iteration_count=ITERATION_COUNT, result_sequence=3
    )
    assert 40 < result < 42.5
    print("Chance of not picking a spade with 3 cards {}%".format(result))


def test_picking_3_suits_in_any_order():
    picking_3_suits_in_any_order = [
        {"action": "start_with", "command": "standard_deck"},
        {"action": "pick", "command": "random_cards", "meta": {"count": 3}},
        {
            "action": "compare_picked",
            "command": "all_match",
            "meta": {
                "conditions": [
                    {
                        "type": "suits",
                        "values": [SUIT_HEARTS, SUIT_DIAMONDS, SUIT_CLUBS],
                    },
                    {
                        "type": "suits",
                        "values": [SUIT_HEARTS, SUIT_DIAMONDS, SUIT_CLUBS],
                    },
                    {
                        "type": "colours",
                        "values": [COLOUR_RED, COLOUR_BLACK, COLOUR_RED],
                    },
                ],
            },
        },
    ]

    lan = Language(sequences=picking_3_suits_in_any_order)
    result = ProbabilityTest.run_language_probability_test(
        lan.execute, iteration_count=ITERATION_COUNT, result_sequence=3
    )
    assert 9 < result < 11
    print("Chance of picking 3 suits in any order is {}%".format(result))


def test_picking_3_suits_in_specific_order():
    """
    Probability of picking diamond, heard, and spade, in this order
    """
    picking_3_suits_in_specific_order = [
        {"action": "start_with", "command": "standard_deck"},
        {"action": "pick", "command": "random_cards", "meta": {"count": 3}},
        {
            "action": "compare_picked",
            "command": "order_match",
            "meta": {
                "suits": [SUIT_HEARTS, SUIT_DIAMONDS, SUIT_CLUBS],
            },
        },
    ]

    lan = Language(sequences=picking_3_suits_in_specific_order)
    result = ProbabilityTest.run_language_probability_test(
        lan.execute, iteration_count=ITERATION_COUNT, result_sequence=3
    )
    assert 1 < result < 2
    print("Chance of picking 3 suits in HDS order is {}%".format(result))
