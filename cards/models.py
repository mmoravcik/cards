import random
from . import constants
from . import exceptions


class Card(object):
    value = None
    suit = None

    def __init__(self, value, suit):
        self.suit = suit
        self.value = value

    @property
    def colour(self):
        return constants.CARD_SUITS_CONF[self.suit]['colour']

    @property
    def suit_symbol(self):
        return constants.CARD_SUITS_CONF[self.suit]['symbol']

    @property
    def value_symbol(self):
        return constants.CARD_VALUES_CONF[self.value]['symbol']

    def is_the_same_card(self, card):
        """
        Compare self.card with card and see if they are the same, e.g. they have
        the same suit and value
        :param card: <Card>
        :return: <bool>
        """
        return self.suit == card.suit and self.value == card.value

    def __str__(self):
        return "{}{}".format(
            self.value_symbol,
            self.suit_symbol
        )

    def __repr__(self):
        return "{}".format(self.__str__())


class StandardDeck(object):
    NUMBER_OF_CARDS = 52
    EACH_CARD_OCCURS = 1
    cards = None

    def __init__(self):
        # Always start with fresh, ordered deck of cards
        self.reset()

    @property
    def is_full(self):
        """
        Is this deck full?
        :return: <bool>
        """
        return len(self.cards) == self.NUMBER_OF_CARDS

    @property
    def is_over_filled(self):
        """
        Is this deck overfilled?
        :return: <bool>
        """
        return len(self.cards) > self.NUMBER_OF_CARDS

    @property
    def is_full_or_overfilled(self):
        return self.is_full or self.is_over_filled

    @property
    def is_valid_deck(self):
        """
        Standard deck has all cards.
        :return: <bool>
        """
        if not self.is_full:
            return False

        for suit in constants.CARD_SUITS_CONF.keys():
            for value in constants.CARD_VALUES_CONF.keys():
                if self.card_occurrence_count(Card(value, suit)) != self.EACH_CARD_OCCURS:
                    return False
        return True

    def card_occurrence_count(self, card):
        """
        How many times is this card in the deck?
        :param card: <Card>
        :return: <int> number of occurrences
        """
        occurrences = 0
        for existing_card in self.cards:
            if existing_card.is_the_same_card(card):
                occurrences += 1
        return occurrences

    def reset(self):
        """
        Reset the deck so it contains all cards in suit / value order
        """
        self.cards = []
        for suit in constants.CARD_SUITS_CONF.keys():
            for value in constants.CARD_VALUES_CONF.keys():
                for _ in range(0, self.EACH_CARD_OCCURS):
                    self.cards.append(Card(value, suit))

    def shuffle(self):
        """
        Shuffle all cards in this deck
        """
        random.shuffle(self.cards)

    def pick_random_card(self):
        """
        Pick a card from the deck, it will also removed it from self.cards

        :return: <Card>
        """
        return self.pick_random_cards(number_of_cards=1)[0]

    def pick_random_cards(self, number_of_cards):
        """
        Pick random cards from the deck, it will also removed it from self.cards

        :param number_of_cards: <int> How many cards to pick?
        :return: <Card[]>
        """
        if number_of_cards > len(self.cards):
            raise exceptions.NotEnoughCardsException()

        picked_cards = list()
        for _ in range(0, number_of_cards):
            picked_cards.append(self.cards.pop(random.randrange(len(self.cards))))
        return picked_cards

    def pick_card(self, card):
        """
        Pick and remove specific card from the deck
        :param card: <Card>
        :return: <Card>
        """
        if self.card_occurrence_count(card) == 0:
            raise exceptions.CardIsNotInTheDeck()

        for idx, existing_card in enumerate(self.cards):
            if existing_card.is_the_same_card(card):
                return self.cards.pop(idx)

    def insert_card(self, card, force=False):
        """
        Insert a card to a deck, but make sure it is not duplicated and deck
        is not full
        If forced, it will insert any card without a check
        :param card: <Card>
        :param force: <bool> Force the card insertion
        """
        if self.is_full_or_overfilled and not force:
            raise exceptions.DeckFullException()

        if not force:
            occurrences = self.card_occurrence_count(card)
            if occurrences > self.EACH_CARD_OCCURS - 1:
                raise exceptions.IncorrectDeckException(
                    "Card `{}` is already in the pack {} time(s)".format(
                        str(card), occurrences
                    )
                )

        self.cards.append(card)

    @staticmethod
    def _get_percentage(success_count, iterations):
        """
        Just a silly helper function to help calculate the percentage value.
        :param success_count: <int> Number of times desired event happened
        :param iterations: <int> Number of times we've tried
        :return: <float> Percentage of success_count of iterations
        """
        return (float(success_count) / float(iterations)) * 100

    @staticmethod
    def run_probability_test(test_func, iteration_count=1000, **kwargs):
        """
        Run test_func over `iteration_count` times and return the probability
        in percent of the event happening
        :param test_func: <function>
        :param iteration_count: <int> how many iterations?
        :return: <float> Percentage of chance of test happening

        Example usage:

        ```
        def test_func(optional_argument):
            '''
            What is the chance that we will pick up a red card from the deck
            of cars?
            '''
            deck = StandardDeck()
            card = deck.pick_random_card()
            return card.colour == COLOUR_RED

        # We expect this to be close to 50%
        result = StandardDeck.run_probability_test(test_func, optional_argument=foo)
        print 'Chance of a red card is {}%'.format(result)
        ```
        """
        success_runs = 0
        for _ in range(0, iteration_count):
            if test_func(**kwargs):
                success_runs += 1
        return StandardDeck._get_percentage(success_runs, iteration_count)


class JokerDeck(StandardDeck):
    """"
    Joker deck is a regular deck included twice.
    TODO Add an actual joker card support
    """
    NUMBER_OF_CARDS = 104
    EACH_CARD_OCCURS = 2
    cards = None
