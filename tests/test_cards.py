from ..cards.models import Card
from ..cards import constants


def test_card_colour():
    card = Card(3, constants.SUIT_SPADES)
    assert card.colour == constants.COLOUR_BLACK

    card = Card(10, constants.SUIT_CLUBS)
    assert card.colour == constants.COLOUR_BLACK

    card = Card(13, constants.SUIT_HEARTS)
    assert card.colour == constants.COLOUR_RED

    card = Card(1, constants.SUIT_DIAMONDS)
    assert card.colour == constants.COLOUR_RED


def test_pretty_card():
    card = Card(3, constants.SUIT_SPADES)
    assert str(card) == '3S'

    card = Card(10, constants.SUIT_CLUBS)
    assert str(card) == '10C'

    card = Card(13, constants.SUIT_HEARTS)
    assert str(card) == 'KH'

    card = Card(1, constants.SUIT_DIAMONDS)
    assert str(card) == 'AD'
