import pytest

from ..cards.models import StandardDeck, Card, StandardDeckWithJokers, Joker

from ..cards import constants
from ..cards import exceptions


def test_shuffle_deck():
    deck = StandardDeck()
    another_deck = StandardDeck()

    sample_size = 10

    assert (
        StandardDeck.NUMBER_OF_NON_JOKER_CARDS
        == len(another_deck.cards)
        == len(deck.cards)
    )
    for i in range(0, sample_size):
        assert str(deck.cards[i]) == str(another_deck.cards[i])

    another_deck.shuffle()
    assert len(another_deck.cards) == StandardDeck.NUMBER_OF_NON_JOKER_CARDS

    assert (
        StandardDeck.NUMBER_OF_NON_JOKER_CARDS
        == len(deck.cards)
        == len(another_deck.cards)
    )

    matching_cards = 0
    for i in range(0, sample_size):
        if str(deck.cards[i]) == str(another_deck.cards[i]):
            matching_cards += 1

    # It is extremely unlikely that X cards will be the same in a shuffled deck
    assert matching_cards < sample_size - 1


def test_pick_random_card():
    deck = StandardDeck()

    picked_card_1 = deck.pick_random_card()
    assert isinstance(picked_card_1, Card)

    assert len(deck.cards) == StandardDeck.NUMBER_OF_NON_JOKER_CARDS - 1

    picked_card_2 = deck.pick_random_card()
    assert isinstance(picked_card_2, Card)

    assert len(deck.cards) == StandardDeck.NUMBER_OF_NON_JOKER_CARDS - 2

    assert picked_card_1 != picked_card_2


def test_pick_random_cards():
    deck = StandardDeck()
    picked_cards = deck.pick_random_cards(4)

    assert StandardDeck.NUMBER_OF_NON_JOKER_CARDS - 4 == len(deck.cards)
    assert 4 == len(picked_cards)

    # we can't pick more that remaining cards
    with pytest.raises(exceptions.NotEnoughCardsException):
        deck.pick_random_cards(StandardDeck.NUMBER_OF_NON_JOKER_CARDS + 1)


def test_pick_card():
    deck = StandardDeck()
    card = Card(13, suit=constants.SUIT_CLUBS)

    assert StandardDeck.NUMBER_OF_NON_JOKER_CARDS == len(deck.cards)
    card = deck.pick_card(card)
    assert card.suit == constants.SUIT_CLUBS
    assert card.value == 13
    assert StandardDeck.NUMBER_OF_NON_JOKER_CARDS - 1 == len(deck.cards)

    # we can't pick the card again as it doesn't exist in the deck
    with pytest.raises(exceptions.CardIsNotInTheDeck):
        deck.pick_card(card)


def test_card_occurrence_count():
    deck = StandardDeck()
    picked_card = deck.pick_random_card()
    assert 0 == deck.card_occurrence_count(picked_card)

    deck.insert_card(picked_card)
    assert 1 == deck.card_occurrence_count(picked_card)

    deck.insert_card(picked_card, force=True)
    assert 2 == deck.card_occurrence_count(picked_card)


def test_bool_properties_standard_deck():
    deck = StandardDeck()
    assert deck.is_full
    assert not deck.is_over_filled
    assert deck.is_full_or_overfilled

    deck.pick_random_card()
    assert not deck.is_full
    assert not deck.is_over_filled
    assert not deck.is_full_or_overfilled

    deck.reset()
    deck.cards.append(Card(constants.SUIT_SPADES, 33))
    assert not deck.is_full
    assert deck.is_over_filled
    assert deck.is_full_or_overfilled


def test_bool_properties_standard_deck_with_jokers():
    deck = StandardDeckWithJokers()
    assert deck.is_full
    assert not deck.is_over_filled
    assert deck.is_full_or_overfilled

    deck.pick_random_card()
    assert not deck.is_full
    assert not deck.is_over_filled
    assert not deck.is_full_or_overfilled

    deck.reset()
    deck.cards.append(Card(constants.SUIT_SPADES, 33))
    assert not deck.is_full
    assert deck.is_over_filled
    assert deck.is_full_or_overfilled


def test_insert_card():
    deck = StandardDeck()
    picked_card = deck.pick_random_card()
    assert len(deck.cards) == StandardDeck.NUMBER_OF_NON_JOKER_CARDS - 1

    deck.insert_card(picked_card)
    assert len(deck.cards) == StandardDeck.NUMBER_OF_NON_JOKER_CARDS
    assert deck.is_valid_deck

    # We can't insert the same card twice, unless forced
    with pytest.raises(exceptions.DeckFullException):
        deck.insert_card(picked_card)
        assert len(deck.cards) == 52

    deck.insert_card(picked_card, force=True)
    assert len(deck.cards) == 53
    assert not deck.is_valid_deck


def test_insert_existing_card():
    deck = StandardDeck()
    picked_cards = deck.pick_random_cards(2)

    assert len(deck.cards) == StandardDeck.NUMBER_OF_NON_JOKER_CARDS - 2
    # Lets try to insert the same card twice, it should not work, unless forced

    deck.insert_card(picked_cards[0], force=False)
    assert len(deck.cards) == StandardDeck.NUMBER_OF_NON_JOKER_CARDS - 1

    with pytest.raises(exceptions.IncorrectDeckException):
        deck.insert_card(picked_cards[0], force=False)

    assert len(deck.cards) == StandardDeck.NUMBER_OF_NON_JOKER_CARDS - 1

    deck.insert_card(picked_cards[0], force=True)
    assert len(deck.cards) == StandardDeck.NUMBER_OF_NON_JOKER_CARDS
    # StandardDeck is not valid as it has the same card twice
    assert not deck.is_valid_deck


def test_insert_existing_card_joker_deck():
    deck = StandardDeckWithJokers()
    # Pick 1 joker
    deck.pick_card(Joker())

    assert (
        len(deck.cards)
        == StandardDeckWithJokers.NUMBER_OF_NON_JOKER_CARDS
        + StandardDeckWithJokers.NUMBER_OF_JOKERS
        - 1
    )
    # 1 Joker is still in pack
    assert 1 == deck.card_occurrence_count(Joker())

    # Lets try to insert the joker 2 times, it should not work, unless forced
    # First one is OK
    deck.insert_card(Joker(), force=False)
    assert (
        len(deck.cards)
        == StandardDeckWithJokers.NUMBER_OF_NON_JOKER_CARDS
        + StandardDeckWithJokers.NUMBER_OF_JOKERS
    )
    assert 2 == deck.card_occurrence_count(Joker())

    # Second raises a deck full exception
    with pytest.raises(exceptions.DeckFullException):
        deck.insert_card(Joker(), force=False)

    deck.insert_card(Joker(), force=True)
    assert (
        len(deck.cards)
        == StandardDeckWithJokers.NUMBER_OF_NON_JOKER_CARDS
        + StandardDeckWithJokers.NUMBER_OF_JOKERS
        + 1
    )
    assert 3 == deck.card_occurrence_count(Joker())
    # StandardDeck is not valid as it has the same card twice
    assert not deck.is_valid_deck


def test_is_valid_deck():
    deck = StandardDeck()
    assert deck.is_valid_deck

    picked_card = deck.pick_random_card()
    assert not deck.is_valid_deck

    deck.insert_card(picked_card)
    assert deck.is_valid_deck

    deck.insert_card(picked_card, force=True)
    assert not deck.is_valid_deck


def test_is_valid_deck_with_jokers():
    deck = StandardDeckWithJokers()
    assert deck.is_valid_deck

    picked_card = deck.pick_random_card()
    assert not deck.is_valid_deck

    deck.insert_card(picked_card)
    assert deck.is_valid_deck

    deck.pick_card(Joker())
    assert not deck.is_valid_deck

    deck.insert_card(Joker())
    assert deck.is_valid_deck

    deck.insert_card(picked_card, force=True)
    assert not deck.is_valid_deck
