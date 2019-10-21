from cards.constants import SUIT_HEARTS, SUIT_DIAMONDS, COLOUR_RED, SUIT_CLUBS
from cards.language import Language
from cards.models import Card, ProbabilityTest


# Probability of picked card being RED
red_card_probability = [
    {
        "action": "start_with",
        "command": "standard_deck"
    },
    {
        "action": "pick",
        "command": "random_cards",
        "meta": {
            "count": 1
        }
    },
    {
        "action": "compare_picked",
        "command": "any_match",
        "meta": {
            "colours": [COLOUR_RED],
            "from_sequence": 2,
        }
    }
]

lan = Language(sequences=red_card_probability)

result = ProbabilityTest.run_probability_test(lan.execute, result_sequence=3)
print('Chance of a red card is {}%'.format(result))


# Probability of high card selected
high_card_probability = [
    {
        "action": "start_with",
        "command": "standard_deck"
    },
    {
        "action": "pick",
        "command": "random_cards",
        "meta": {
            "count": 5
        }
    },
    {
        "action": "compare_picked",
        "command": "any_match",
        "meta": {
            "values": [1, 13, 12, 11, 10],
            "matches_required": 1,
        }
    }
]

lan = Language(sequences=high_card_probability)
result = ProbabilityTest.run_probability_test(lan.execute, result_sequence=3)
print('Chance of a high card is {}%'.format(result))


# Probability of cutting a joker
cutting_a_joker_probability = [
    {
        "action": "start_with",
        "command": "canasta_deck"
    },
    {
        "action": "pick",
        "command": "random_cards",
        "meta": {
            "count": 3
        }
    },
    {
        "action": "compare_picked",
        "command": "any_match",
        "meta": {
            "values": ["*"],
            "matches_required": 1,
        }
    }
]

lan = Language(sequences=cutting_a_joker_probability)
result = ProbabilityTest.run_probability_test(lan.execute, result_sequence=3)
print('Chance of cutting a joker is {}%'.format(result))


cutting_two_jokers_probability = cutting_a_joker_probability
cutting_two_jokers_probability[2]["meta"]["matches_required"] = 2

lan = Language(sequences=cutting_two_jokers_probability)
result = ProbabilityTest.run_probability_test(lan.execute, result_sequence=3)
print('Chance of cutting two jokers is {}%'.format(result))


# Probability of picking a single specific card
picking_a_single_specific_card = [
    {
        "action": "start_with",
        "command": "standard_deck"
    },
    {
        "action": "pick",
        "command": "random_cards",
        "meta": {
            "count": 1
        }
    },
    {
        "action": "compare_picked",
        "command": "any_match",
        "meta": {
            "cards": [Card(value=1, suit=SUIT_HEARTS)],
            "matches_required": 1,
        }
    }
]

lan = Language(sequences=picking_a_single_specific_card)
result = ProbabilityTest.run_probability_test(lan.execute, result_sequence=3)
print('Chance of picking an ace of hearths is {}%'.format(result))


# Probability of picking 2 specific card of 26 picked
picking_specific_2_cards_out_of_26 = [
    {
        "action": "start_with",
        "command": "standard_deck"
    },
    {
        "action": "pick",
        "command": "random_cards",
        "meta": {
            "count": 26
        }
    },
    {
        "action": "compare_picked",
        "command": "any_match",
        "meta": {
            "cards": [Card(value=1, suit=SUIT_HEARTS), Card(value=2, suit=SUIT_HEARTS)],
            "matches_required": 2,
        }
    }
]

lan = Language(sequences=picking_specific_2_cards_out_of_26)
result = ProbabilityTest.run_probability_test(lan.execute, result_sequence=3)
print('Chance of picking specific 2 cards out of 26 is {}%'.format(result))


# Probability of picking 3 cards and not a spade
picking_3_cards_no_spade = [
    {
        "action": "start_with",
        "command": "standard_deck"
    },
    {
        "action": "pick",
        "command": "random_cards",
        "meta": {
            "count": 3
        }
    },
    {
        "action": "compare_picked",
        "command": "any_match",
        "meta": {
            "suits": [SUIT_HEARTS, SUIT_DIAMONDS, SUIT_CLUBS],
            "matches_required": 3,
        }
    }
]

lan = Language(sequences=picking_3_cards_no_spade)
result = ProbabilityTest.run_probability_test(lan.execute, result_sequence=3)
print('Chance of not picking a spade with 3 cards {}%'.format(result))


# Probability of picking diamond, heard, and spade, in any order
picking_3_suits_in_any_order = [
    {
        "action": "start_with",
        "command": "standard_deck"
    },
    {
        "action": "pick",
        "command": "random_cards",
        "meta": {
            "count": 3
        }
    },
    {
        "action": "compare_picked",
        "command": "all_match",
        "meta": {
            "suits": [SUIT_HEARTS, SUIT_DIAMONDS, SUIT_CLUBS],
        }
    }
]

lan = Language(sequences=picking_3_suits_in_any_order)
result = ProbabilityTest.run_probability_test(lan.execute, result_sequence=3)
print('Chance of picking 3 suits in any order is {}%'.format(result))


# Probability of picking diamond, heard, and spade, in this order
picking_3_suits_in_specific_order = [
    {
        "action": "start_with",
        "command": "standard_deck"
    },
    {
        "action": "pick",
        "command": "random_cards",
        "meta": {
            "count": 3
        }
    },
    {
        "action": "compare_picked",
        "command": "order_match",
        "meta": {
            "suits": [SUIT_HEARTS, SUIT_DIAMONDS, SUIT_CLUBS],
        }
    }
]

lan = Language(sequences=picking_3_suits_in_specific_order)
result = ProbabilityTest.run_probability_test(lan.execute, result_sequence=3)
print('Chance of picking 3 suits in HDS order is {}%'.format(result))