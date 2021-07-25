import pytest

from ..cards.exceptions import UnsupportedDeckType, NotEnoughCardsException, CardIsNotInTheDeck
from ..cards.constants import (
    SUIT_HEARTS,
    SUIT_DIAMONDS,
    COLOUR_RED,
    SUIT_CLUBS,
    COLOUR_BLACK,
)
from ..cards.language import Language
from ..cards.models import ProbabilityTest, StandardDeck, JokerDeck, Card

ITERATION_COUNT = 15000

pytestmark = pytest.mark.slow

@pytest.fixture
def standard_deck_sequence():
    return [{
        "command": "init_deck",
        "meta": {
            "deck_type": "standard_deck"
        },
    }]


def test_init_known_deck():
    sequences = [{
        "command": "init_deck",
        "meta": {
            "deck_type": "standard_deck"
        },

    }, {
        "command": "init_deck",
        "meta": {
            "deck_type": "canasta_deck"
        },

    }]
    lan = Language(sequences=sequences)
    lan.execute()
    assert lan.sequence_results[1].__class__ == StandardDeck
    assert lan.sequence_results[2].__class__ == JokerDeck


def test_init_unknown_deck():
    sequences = [{
        "command": "init_deck",
        "meta": {
            "deck_type": "random_lalala"
        }
    }]
    lan = Language(sequences=sequences)
    with pytest.raises(UnsupportedDeckType):
        lan.execute()


def test_pick_random_cards_from_deck(standard_deck_sequence):
    sequences = standard_deck_sequence
    sequences.append({
        "command": "pick_random_cards",
        "meta": {
            "count": 10,
            "from_sequence": 1
        }
    })
    lan = Language(sequences=sequences)
    lan.execute()
    result = lan.sequence_results[2]
    assert len(result) == 10
    assert len(set(result)) == 10  # are they all unique?
    for card in result:
        # Check that we picked cards indeed
        assert card.__class__ == Card


def test_pick_random_cards_from_sequence(standard_deck_sequence):
    sequences = standard_deck_sequence
    sequences.append({
        "command": "pick_random_cards",
        "meta": {
            "count": 10,
            "from_sequence": 1
        }
    })
    sequences.append({
        "command": "pick_random_cards",
        "meta": {
            "count": 5,
            "from_sequence": 2
        }
    })
    lan = Language(sequences=sequences)
    lan.execute()
    result = lan.sequence_results[3]
    assert len(result) == 5
    assert len(set(result)) == 5  # are they all unique?
    for card in result:
        # Check that we picked cards indeed
        assert card.__class__ == Card
        # And they are coming from the right sequence
        assert card in lan.sequence_results[2]


def test_pick_too_many_cards_from_deck_at_once(standard_deck_sequence):
    sequences = standard_deck_sequence
    sequences.append({
        "command": "pick_random_cards",
        "meta": {
            "count": 105,  # too many cards
            "from_sequence": 1
        }
    })
    lan = Language(sequences=sequences)
    with pytest.raises(NotEnoughCardsException):
        lan.execute()


def test_pick_too_many_cards_from_deck_sequentially(standard_deck_sequence):
    sequences = standard_deck_sequence
    sequences.append({
        "command": "pick_random_cards",
        "meta": {
            "count": int(52 / 2),
            "from_sequence": 1
        }
    })
    sequences.append({
        "command": "pick_random_cards",
        "meta": {
            "count": int(52 / 2) + 1,
            "from_sequence": 1
        }
    })
    lan = Language(sequences=sequences)
    with pytest.raises(NotEnoughCardsException):
        lan.execute()


def test_pick_specific_cards_from_deck(standard_deck_sequence):
    sequences = standard_deck_sequence
    sequences.append({
        "command": "pick_specific_cards",
        "meta": {
            "cards": [
                {"value": 13, "suit": "hearts"},
                {"value": 3, "suit": "spades"},
            ],
            "from_sequence": 1
        }
    })
    lan = Language(sequences=sequences)
    lan.execute()
    result = lan.sequence_results[2]
    assert len(result) == 2
    king_of_hearts = Card(value=13, suit="hearts")
    three_of_spades = Card(value=3, suit="spades")
    assert king_of_hearts in result
    assert three_of_spades in result


def test_pick_specific_cards_from_sequence(standard_deck_sequence):
    sequences = standard_deck_sequence
    sequences.append({
        "command": "pick_specific_cards",
        "meta": {
            "cards": [
                {"value": 13, "suit": "hearts"},
                {"value": 3, "suit": "spades"},
                {"value": 2, "suit": "diamonds"},
            ],
            "from_sequence": 1
        }
    })
    sequences.append({
        "command": "pick_specific_cards",
        "meta": {
            "cards": [
                {"value": 13, "suit": "hearts"},
                {"value": 3, "suit": "spades"},
            ],
            "from_sequence": 2
        }
    })

    lan = Language(sequences=sequences)
    lan.execute()
    result = lan.sequence_results[3]
    assert len(result) == 2
    assert len(lan.sequence_results[2]) == 3
    king_of_hearts = Card(value=13, suit="hearts")
    three_of_spades = Card(value=3, suit="spades")
    assert king_of_hearts in result
    assert three_of_spades in result


def test_pick_unknown_specific_cards_from_sequence(standard_deck_sequence):
    sequences = standard_deck_sequence
    sequences.append({
        "command": "pick_specific_cards",
        "meta": {
            "cards": [
                {"value": 13, "suit": "hearts"},
                {"value": 3, "suit": "spades"},
                {"value": 2, "suit": "diamonds"},
            ],
            "from_sequence": 1
        }
    })
    sequences.append({
        "command": "pick_specific_cards",
        "meta": {
            "cards": [
                {"value": 4, "suit": "hearts"},  # this card doesn't exists in seq #2
                {"value": 3, "suit": "spades"},
            ],
            "from_sequence": 2
        }
    })

    lan = Language(sequences=sequences)
    with pytest.raises(CardIsNotInTheDeck):
        lan.execute()


def test_shuffle_deck(standard_deck_sequence):
    sequences = standard_deck_sequence
    lan = Language(sequences=standard_deck_sequence)
    lan.execute()
    first_card = lan.sequence_results[1].cards[0]
    second_card = lan.sequence_results[1].cards[1]
    third_card = lan.sequence_results[1].cards[2]
    sequences.append({
        "command": "shuffle",
        "meta": {
            "sequence": 1
        }
    })
    lan.execute()
    first_card_2 = lan.sequence_results[2].cards[0]
    second_card_2 = lan.sequence_results[2].cards[1]
    third_card_2 = lan.sequence_results[2].cards[2]

    assert any([
        first_card != first_card_2,
        second_card != second_card_2,
        third_card != third_card_2,
    ])


def test_shuffle_sequence(standard_deck_sequence):
    sequences = standard_deck_sequence
    sequences.append({
        "command": "pick_random_cards",
        "meta": {
            "count": 10,
            "from_sequence": 1
        }
    })
    lan = Language(sequences=standard_deck_sequence)
    lan.execute()
    first_card = lan.sequence_results[2][0]
    second_card = lan.sequence_results[2][1]
    third_card = lan.sequence_results[2][2]

    sequences.append({
        "command": "shuffle",
        "meta": {
            "sequence": 2
        }
    })
    lan.execute()
    first_card_2 = lan.sequence_results[2][0]
    second_card_2 = lan.sequence_results[2][1]
    third_card_2 = lan.sequence_results[2][2]

    assert any([
        first_card != first_card_2,
        second_card != second_card_2,
        third_card != third_card_2,
    ])
