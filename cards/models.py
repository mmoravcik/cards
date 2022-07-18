import random
from dataclasses import dataclass

from itertools import product

from . import constants
from . import exceptions


@dataclass
class Card:
    value: int
    suit: str

    @property
    def colour(self):
        if self.is_joker:
            return '*'
        return constants.CARD_SUITS_CONF[self.suit]['colour']

    @property
    def suit_symbol(self):
        if self.is_joker:
            return '*'
        return constants.CARD_SUITS_CONF[self.suit]['symbol']

    @property
    def value_symbol(self):
        if self.is_joker:
            return '*'
        return constants.CARD_VALUES_CONF[self.value]['symbol']

    @property
    def is_joker(self):
        return self == Joker() or (
            self.suit == constants.JOKER_SUIT and self.value == constants.JOKER_VALUE
        )

    def __str__(self):
        return "{}{}".format(
            self.value_symbol,
            self.suit_symbol,
        )

    def __hash__(self):
        return hash((self.value, self.suit))

    def __repr__(self):
        return "{}".format(self.__str__())


@dataclass
class Joker(Card):
    value: str = constants.JOKER_VALUE
    suit: str = constants.JOKER_SUIT


class StandardDeck(object):
    NUMBER_OF_NON_JOKER_CARDS = 52
    EACH_NON_JOKER_CARD_OCCURS = 1
    NUMBER_OF_JOKERS = 0
    cards = None

    def __init__(self):
        # Always start with fresh, ordered deck of cards
        self.reset()

    @property
    def is_full(self) -> bool:
        """
        Is this deck full?
        :return: <bool>
        """
        return len(self.cards) == self.NUMBER_OF_NON_JOKER_CARDS + self.NUMBER_OF_JOKERS

    @property
    def is_over_filled(self) -> bool:
        """
        Is this deck overfilled?
        :return: <bool>
        """
        return len(self.cards) > self.NUMBER_OF_NON_JOKER_CARDS + self.NUMBER_OF_JOKERS

    @property
    def is_full_or_overfilled(self) -> bool:
        return self.is_full or self.is_over_filled

    @property
    def is_valid_deck(self) -> bool:
        """
        Standard deck has all cards.
        :return: <bool>
        """
        if not self.is_full:
            return False

        for p in product(
            constants.CARD_SUITS_CONF.keys(),
            constants.CARD_VALUES_CONF.keys(),
        ):
            card = Card(suit=p[0], value=p[1])
            if self.card_occurrence_count(card) != self.EACH_NON_JOKER_CARD_OCCURS:
                return False
        return True

    def card_occurrence_count(self, card: Card) -> int:
        """
        How many times is this card in the deck?
        :param card: <Card>
        :return: <int> number of occurrences
        """
        return self.cards.count(card)

    def reset(self) -> None:
        """
        Reset the deck so it contains all cards in suit / value order
        """
        self.cards = []
        for _ in range(0, self.EACH_NON_JOKER_CARD_OCCURS):
            for p in product(
                constants.CARD_SUITS_CONF.keys(),
                constants.CARD_VALUES_CONF.keys(),
            ):
                self.cards.append(Card(value=p[1], suit=p[0]))

        for _ in range(0, self.NUMBER_OF_JOKERS):
            self.cards.append(Joker())

    def shuffle(self) -> None:
        """
        Shuffle all cards in this deck
        """
        random.shuffle(self.cards)

    def pick_random_card(self) -> Card:
        """
        Pick a card from the deck, it will also removed it from self.cards

        :return: <Card>
        """
        return self.pick_random_cards(number_of_cards=1)[0]

    def pick_random_cards(self, number_of_cards: int) -> list[Card]:
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

    def pick_card(self, card: Card) -> Card:
        """
        Pick and remove specific card from the deck
        :param card: <Card>
        :return: <Card>
        """
        if self.card_occurrence_count(card) == 0:
            raise exceptions.CardIsNotInTheDeck()

        for idx, existing_card in enumerate(self.cards):
            if existing_card == card:
                return self.cards.pop(idx)

    def insert_card(self, card: Card, force: bool = False) -> None:
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
            if any([
                card.is_joker and occurrences > self.NUMBER_OF_JOKERS - 1,
                not card.is_joker and occurrences > self.EACH_NON_JOKER_CARD_OCCURS - 1,
            ]):
                raise exceptions.IncorrectDeckException(
                    "Card `{}` is already in the deck {} time(s)".format(
                        str(card), occurrences
                    )
                )
        self.cards.append(card)


class ProbabilityTest(object):
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
    def run_language_probability_test(test_func, result_sequence, iteration_count=20000, **kwargs):
        """
        Run test_func over `iteration_count` times and return the probability
        in percent of the event happening
        :param test_func: <function>
        :param result_sequence: <int> which sequence returns the final Bool?
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
        successful_runs = 0
        for _ in range(0, iteration_count):
            if test_func(**kwargs)[result_sequence]:
                successful_runs += 1
        return ProbabilityTest._get_percentage(successful_runs, iteration_count)

    @staticmethod
    def run_probability_test(test_func, iteration_count=20000, **kwargs):
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
        result = ProbabilityTest.run_probability_test(test_func, optional_argument=foo)
        print 'Chance of a red card is {}%'.format(result)
        ```
        """
        successful_runs = 0
        for _ in range(0, iteration_count):
            if test_func(**kwargs):
                successful_runs += 1
        return ProbabilityTest._get_percentage(successful_runs, iteration_count)


class StandardDeckWithJokers(StandardDeck):
    NUMBER_OF_NON_JOKER_CARDS = 52
    NUMBER_OF_JOKERS = 2


class JokerDeck(StandardDeck):
    """"
    Joker deck is a regular deck included twice.
    """
    NUMBER_OF_NON_JOKER_CARDS = 104
    EACH_NON_JOKER_CARD_OCCURS = 2
    NUMBER_OF_JOKERS = 4


class EmptyDeck(StandardDeck):
    """"
    Deck with no cards
    """
    NUMBER_OF_NON_JOKER_CARDS = 0
    EACH_NON_JOKER_CARD_OCCURS = 0
    NUMBER_OF_JOKERS = 0
