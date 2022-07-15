import random

import pytest

from ..cards.constants import COLOUR_BLACK
from ..cards.models import (
    StandardDeck,
    JokerDeck,
    Card,
    EmptyDeck,
    ProbabilityTest,
)
from ..cards import constants

ITERATION_COUNT = 15000

pytestmark = pytest.mark.slow


def test_high_card_is_selected():
    def fn():
        deck = StandardDeck()
        deck.shuffle()
        picked_cards = deck.pick_random_cards(5)
        for card in picked_cards:
            # 1 is Ace, high card for my purpose
            if card.value in [1, 10, 11, 12, 13]:
                return True
        return False

    result = ProbabilityTest.run_probability_test(fn, iteration_count=ITERATION_COUNT)
    assert 91 < result < 93
    print('High card has been picked in {}% cases'.format(result))


def test_same_card_is_turned_face_up():
    """
    You have two decks and you turn a card from both at once.
    What is the probability that it will be the same card at least once?
    """
    def fn():
        deck1 = StandardDeck()
        deck2 = StandardDeck()
        deck1.shuffle()
        deck2.shuffle()

        for i in range(0, 52):
            if str(deck1.cards[i]) == str(deck2.cards[i]):
                return True
        return False

    result = ProbabilityTest.run_probability_test(fn, iteration_count=ITERATION_COUNT)
    assert 62 < result < 64.5
    print('Same card has been discovered in {}% cases'.format(result))


def test_pick_red_card():
    """
    What is the chance that we will pick up a red card from deck
    of cars?
    """

    def fn():
        deck = StandardDeck()
        card = deck.pick_random_card()
        return card.colour == constants.COLOUR_RED

    # We expect this to be close to 50%
    result = ProbabilityTest.run_probability_test(fn, iteration_count=ITERATION_COUNT)
    assert 49 < result < 51
    print('Chance of a red card is {}%'.format(result))


def test_probability_of_cutting_a_joker():
    """
    What is the chance of picking up a Joker by randomly selecting 3 cards?
    """

    def fn(how_many_jokers_do_i_want=1):
        deck = JokerDeck()
        deck.shuffle()

        assert len(deck.cards) == 108
        # lets pick 3 random cards, and hope we got a joker!
        cards = deck.pick_random_cards(3)

        jokers = 0
        for card in cards:
            if card.is_joker:
                jokers += 1
        return jokers >= how_many_jokers_do_i_want

    result = ProbabilityTest.run_probability_test(
        fn, iteration_count=ITERATION_COUNT, how_many_jokers_do_i_want=1)
    assert 10 < result < 12
    print('Probability of getting at least 1 joker is {}%'.format(result))

    result = ProbabilityTest.run_probability_test(
        fn, iteration_count=ITERATION_COUNT, how_many_jokers_do_i_want=2)
    assert 0 < result < 0.8
    print('Probability of getting at least 2 jokers is {}%'.format(result))


def test_exploding_kittens_dying_in_the_first_round():
    """
    What happened today...My defuse has been stolen before my turn and then
    I've picked up the Exploding kitten straight away.
    What are the odds of this?

    Jack of Hearths will be our Defuse and
    Queen of Hearts will be our Exploding Kitten
    # TODO: make sure that the test is correct...and make sure it is using a right
    amount of cards
    """

    def fn():
        deck = StandardDeck()
        # there are 40 + 20 cards roughly
        king_of_spades = Card(13, constants.SUIT_SPADES)
        # so lets fill the deck with fluff - king of spades
        for x in range(60 - len(deck.cards)):
            deck.insert_card(king_of_spades, force=True)

        defuse = Card(11, constants.SUIT_HEARTS)
        exploding_kitten = Card(12, constants.SUIT_HEARTS)

        # Lets deal "defuse" to player 1, among with 6 other cards
        player_1_cards = [deck.pick_card(defuse)]
        for x in range(1, 6):
            card = Card(value=x, suit=constants.SUIT_CLUBS)
            player_1_cards += [deck.pick_card(card)]

        player_2_cards = []
        for x in range(0, 6):
            card = Card(value=x + 1, suit=constants.SUIT_DIAMONDS)
            player_2_cards += [deck.pick_card(card)]

        # now lets pick defuse from player 1 and at the same time that player
        # will pick up an exploding kitten
        card = player_1_cards.pop(random.randrange(len(player_1_cards)))
        if defuse == card:
            # After picking defuse from player 1, player 2 now picks up
            # non-exploding kitten card
            deck.pick_card(Card(value=10, suit=constants.SUIT_HEARTS))
            # Player 1, now without defuse, is picking up the card, hoping it is
            # not an Exploding kitten
            second_card = deck.pick_random_card()
            if second_card == exploding_kitten:
                return True

    result = ProbabilityTest.run_probability_test(fn, iteration_count=ITERATION_COUNT)
    assert 0.2 < result < 0.45
    print('Probability of dying in the first round of Exploding kittens is {}%'.format(result))


def test_probability_of_winning_a_price_in_3_card_problem():
    """
    What is the 3 'card' problem?
    It is an adaptation of a Monty Hall problem:
    '
    Suppose you're on a game show, and you're given the choice of three doors:
    Behind one door is a car; behind the others, goats.
    You pick a door, say No. 1, and the host, who knows what's behind the doors,
    opens another door, say No. 3, which has a goat.
    He then says to you, "Do you want to pick door No. 2?"
    Is it to your advantage to switch your choice?'
    '

    For our test, the joker is a winning card, and 2 queen of hearts are goats
    """

    def fn():
        deck = EmptyDeck()
        joker = Card(constants.JOKER_VALUE, constants.JOKER_SUIT)
        goat = Card(12, constants.SUIT_HEARTS)
        deck.insert_card(joker, force=True)
        deck.insert_card(goat, force=True)
        deck.insert_card(goat, force=True)
        deck.shuffle()
        assert len(deck.cards) == 3

        random_cards = deck.pick_random_cards(3)

        # host knows which card is a joker
        for idx, card in enumerate(random_cards):
            if card.is_joker:
                joker_index = idx

        # Spectator always selects the first card first
        chosen_card = random_cards[0]

        # The presenter knows which card is not winning, so player
        # can switch to the other card
        if joker_index in [1, 2]:
            chosen_card = random_cards[joker_index]

        if joker_index == 0:
            chosen_card = random_cards[1]

        return chosen_card.is_joker

    result = ProbabilityTest.run_probability_test(fn, iteration_count=ITERATION_COUNT)
    assert 64 < result < 67
    print('Probability picking the winning card is {}%'.format(result))


def test_probability_of_all_dealt_cards_are_red_in_joker():
    def fn():
        deck = JokerDeck()
        dealt_cards = deck.pick_random_cards(14)
        for card in dealt_cards:
            if card.colour == COLOUR_BLACK:
                return False
        return True

    result = ProbabilityTest.run_probability_test(fn, iteration_count=ITERATION_COUNT)
    assert result < 0.5
    print('Probability of all cards being red is {}%'.format(result))


def test_probability_of_all_dealt_cards_are_same_colour_in_joker():
    def fn():
        deck = JokerDeck()
        dealt_cards = deck.pick_random_cards(14)
        desired_colour = dealt_cards[0].colour
        for card in dealt_cards:
            if card.colour == desired_colour:
                return False
        return True

    result = ProbabilityTest.run_probability_test(fn, iteration_count=ITERATION_COUNT)
    assert result < 0.5
    print('Probability of all cards being red is {}%'.format(result))


def test_probability_of_flush_in_5_card_poker():
    def fn():
        deck = StandardDeck()
        dealt_cards = deck.pick_random_cards(5)
        suit_to_match = dealt_cards[0].suit
        for card in dealt_cards:
            if card.suit != suit_to_match:
                return False
        return True

    result = ProbabilityTest.run_probability_test(fn, iteration_count=ITERATION_COUNT)
    assert result < 0.5
    print('Probability of a flush in 5 card poker {}%'.format(result))


def test_probability_of_straight_in_5_card_poker():
    def fn():
        deck = StandardDeck()
        dealt_cards = sorted(deck.pick_random_cards(5), key=lambda x: x.value)
        for idx, card in enumerate(dealt_cards[1:]):
            if card.value - 1 != dealt_cards[idx].value:
                return False
        return True

    result = ProbabilityTest.run_probability_test(fn, iteration_count=ITERATION_COUNT)
    assert 0.2 < result < 0.4
    print('Probability of a straight in poker {}%'.format(result))


def test_probability_of_picking_ace_of_hearths():
    def fn():
        deck = StandardDeck()
        picked = deck.pick_random_card()
        if picked.value == 1 and picked.suit == constants.SUIT_HEARTS:
            return True
        return False

    result = ProbabilityTest.run_probability_test(fn, iteration_count=ITERATION_COUNT)
    assert 1.6 < result < 2.5
    print('Probability of picking an ACE OF HEARTHS is {}%'.format(result))
