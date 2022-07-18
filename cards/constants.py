# -*- coding: utf-8 -*-
COLOUR_RED = "red"
COLOUR_BLACK = "black"

SUIT_HEARTS = "hearts"
SUIT_SPADES = "spades"
SUIT_DIAMONDS = "diamonds"
SUIT_CLUBS = "clubs"

CARD_VALUES_CONF = {
    1: {"symbol": "A"},
    2: {"symbol": "2"},
    3: {"symbol": "3"},
    4: {"symbol": "4"},
    5: {"symbol": "5"},
    6: {"symbol": "6"},
    7: {"symbol": "7"},
    8: {"symbol": "8"},
    9: {"symbol": "9"},
    10: {"symbol": "10"},
    11: {"symbol": "J"},
    12: {"symbol": "Q"},
    13: {"symbol": "K"},
}

CARD_SUITS_CONF = {
    SUIT_SPADES: {"colour": COLOUR_BLACK, "symbol": "♠"},
    SUIT_HEARTS: {"colour": COLOUR_RED, "symbol": "♥"},
    SUIT_CLUBS: {"colour": COLOUR_BLACK, "symbol": "♣"},
    SUIT_DIAMONDS: {"colour": COLOUR_RED, "symbol": "♦"},
}

JOKER_VALUE = "*"
JOKER_SUIT = "*"
