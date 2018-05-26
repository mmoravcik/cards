from cards.models import StandardDeck, JokerDeck, Card
from cards import constants


def test_high_card_is_selected():
    deck = StandardDeck()
    deck.shuffle()
    picked_cards = deck.pick_random_cards(5)
    for card in picked_cards:
        # 1 is Ace, high card for my purpose
        if card.value in [1, 10, 11, 12, 13]:
            return True
    return False


result = StandardDeck.run_probability_test(test_high_card_is_selected)
print('High card has been picked in {}% cases'.format(result))


def test_same_card_is_turned_face_up():
    deck = StandardDeck()
    deck1 = StandardDeck()
    deck.shuffle()
    deck1.shuffle()

    for i in range(0, 52):
        if str(deck.cards[i]) == str(deck1.cards[i]):
            return True
    return False


result = StandardDeck.run_probability_test(test_same_card_is_turned_face_up)
print('Same card has been discovered in {}% cases'.format(result))


def pick_red_card():
    """
    What is the chance that we will pick up a black card from deck
    of cars?
    """
    deck = StandardDeck()
    card = deck.pick_random_card()
    return card.colour == constants.COLOUR_RED


# We expect this to be close to 50%
result = StandardDeck.run_probability_test(pick_red_card)
print('Chance of a black card is {}%'.format(result))


def probability_of_cutting_a_joker(how_many_jokers_do_i_want):
    """
    What is the chance of picking up a Joker by randomly selecting 3 cards?
    """
    deck = JokerDeck()

    # We need to insert 4 extra cards, as we need 4 jokers for this test
    # Lets pretend king of spades is our joker :)
    # Lets add 2 more Kings of spades so we have 4 of them total in the pack
    # And then add 2 more random card, so we have 108 total cards
    king_of_spades = Card(13, constants.SUIT_SPADES)

    deck.insert_card(king_of_spades, force=True)
    deck.insert_card(king_of_spades, force=True)
    deck.insert_card(Card(2, constants.SUIT_DIAMONDS), force=True)
    deck.insert_card(Card(1, constants.SUIT_HEARTS), force=True)
    deck.shuffle()

    assert len(deck.cards) == 108
    # Lets check we have our 4 jokers (Kings of Spades)
    assert deck.card_occurrence_count(king_of_spades) == 4
    # lets pick 3 random cards, and hope we got a joker!
    cards = deck.pick_random_cards(3)

    jokers = 0
    for card in cards:
        if card.value == 13 and card.suit == constants.SUIT_SPADES:
            jokers += 1
    return jokers >= how_many_jokers_do_i_want


result = StandardDeck.run_probability_test(probability_of_cutting_a_joker, how_many_jokers_do_i_want=1)
print('Probability of getting at least 1 joker is {}%'.format(result))

result = StandardDeck.run_probability_test(probability_of_cutting_a_joker, how_many_jokers_do_i_want=2)
print('Probability of getting at least 2 jokers is {}%'.format(result))
