# -*- coding: utf-8 -*-
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

    card = Card(constants.JOKER_VALUE, constants.JOKER_SUIT)
    assert card.colour == '*'


def test_pretty_card():
    card = Card(3, constants.SUIT_SPADES)
    assert str(card) == '3♠'

    card = Card(10, constants.SUIT_CLUBS)
    assert str(card) == '10♣'

    card = Card(13, constants.SUIT_HEARTS)
    assert str(card) == 'K♥'

    card = Card(1, constants.SUIT_DIAMONDS)
    assert str(card) == 'A♦'

    card = Card(constants.JOKER_VALUE, constants.JOKER_SUIT)
    assert str(card) == '**'


def test_is_the_same_card():
    card1 = Card(3, constants.SUIT_SPADES)
    card2 = Card(4, constants.SUIT_HEARTS)
    card3 = Card(5, constants.SUIT_DIAMONDS)
    card4 = Card(6, constants.SUIT_SPADES)
    card5 = Card(3, constants.SUIT_HEARTS)
    # The only card that actually matches card1
    card6 = Card(3, constants.SUIT_SPADES)
    card7 = Card(constants.JOKER_VALUE, constants.JOKER_SUIT)

    assert card1 != card2
    assert card1 != card3
    assert card1 != card4
    assert card1 != card5
    assert card1 == card6
    assert card1 != card7


def test_joker_card():
    card = Card(constants.JOKER_VALUE, constants.JOKER_SUIT)
    assert card.is_joker
