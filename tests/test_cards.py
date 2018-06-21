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


def test_is_the_same_card():
    card1 = Card(3, constants.SUIT_SPADES)
    card2 = Card(4, constants.SUIT_HEARTS)
    card3 = Card(5, constants.SUIT_DIAMONDS)
    card4 = Card(6, constants.SUIT_SPADES)
    card5 = Card(3, constants.SUIT_HEARTS)
    card6 = Card(3, constants.SUIT_SPADES)

    assert card1.is_the_same_card(card2) is False
    assert card1.is_the_same_card(card3) is False
    assert card1.is_the_same_card(card4) is False
    assert card1.is_the_same_card(card5) is False
    assert card1.is_the_same_card(card6) is True
