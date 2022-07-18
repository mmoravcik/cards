from copy import copy, deepcopy
from typing import Union, Iterable

from .exceptions import (
    UnsupportedAction,
    UnsupportedCommand,
    UnsupportedDeckType,
    BadSource,
)
from .models import EmptyDeck, StandardDeck, StandardDeckWithJokers, JokerDeck, Card


class Language(object):
    sequence_results = {}
    current_sequence = None

    AVAILABLE_COMMANDS = [
        "init_deck",
        "pick_random_cards",
        "pick_specific_cards",
        "shuffle",
        "insert_specific_cards",
        "insert_random_cards",
    ]

    def __init__(self, sequences):
        self.sequences = sequences

    def execute_sequence(self, command: AVAILABLE_COMMANDS, **kwargs):
        if command not in self.AVAILABLE_COMMANDS:
            raise UnsupportedCommand()
        return getattr(self, "command_" + command)(**kwargs)

    def execute(self):
        self.current_sequence = 1
        self.sequence_results = {}
        for sequence in self.sequences:
            self.sequence_results[self.current_sequence] = self.execute_sequence(
                command=sequence["command"], **sequence.get("meta", {})
            )
            self.current_sequence += 1
        return self.sequence_results

    # def action_compare_picked(self, command: AVAILABLE_COMMANDS, conditions=None, colours=None, suits=None, cards=None, from_sequence=None, values=None, matches_required=1):
    #     if from_sequence is None:
    #         # We are comparing picked cards from a previous sequence by default
    #         from_sequence = self.current_sequence - 1
    #
    #     # Make sure that removing elements from these array won't affect global scale
    #     suits = copy(suits)
    #     colours = copy(colours)
    #     cards = copy(cards)
    #     values = copy(values)
    #     if command == "any_match":
    #         matches = 0
    #         for card in self.sequence_results[from_sequence]:
    #             for condition in conditions or []:
    #                 if condition["type"] == "colours":
    #                     if card.colour in condition["values"]:
    #                         matches += 1
    #                 elif condition["type"] == "values":
    #                     if card.value in condition["values"]:
    #                         matches += 1
    #                 elif condition["type"] == "specific_cards":
    #                     for specific_card in condition["values"]:
    #                         _card = Card(value=specific_card["value"], suit=specific_card["suit"])
    #                         if card == _card:
    #                             matches += 1
    #                 elif condition["type"] == "suits":
    #                     if card.suit in condition["values"]:
    #                         matches += 1
    #         return matches_required <= matches
    #     elif command == "all_match":
    #         for cond in conditions or []:
    #             condition_values = copy(cond["values"])
    #             for card in self.sequence_results[from_sequence]:
    #                 if cond["type"] == "colours":
    #                     if card.colour not in condition_values:
    #                         return False
    #                     else:
    #                         condition_values.remove(card.colour)
    #                 elif cond["type"] == "values":
    #                     if card.value not in condition_values:
    #                         return False
    #                     else:
    #                         condition_values.remove(card.value)
    #                 elif cond["type"] == "specific_cards":
    #                     if card not in [Card(value=c["value"], suit=c["suit"]) for c in condition_values]:
    #                         return False
    #                     else:
    #                         condition_values.remove({"value": card.value, "suit": card.suit})
    #                 elif cond["type"] == "suits":
    #                     if card.suit not in condition_values:
    #                         return False
    #                     else:
    #                         condition_values.remove(card.suit)
    #         return True
    #     elif command == "order_match":
    #         for idx, card in enumerate(self.sequence_results[from_sequence]):
    #             if colours:
    #                 if card.colour != colours[idx]:
    #                     return False
    #             elif values:
    #                 if card.value != values[idx]:
    #                     return False
    #             elif cards:
    #                 if card != [Card(value=c["value"], suit=c["suit"]) for c in cards][idx]:
    #                     return False
    #             elif suits:
    #                 if card.suit != suits[idx]:
    #                     return False
    #         return True

    def command_init_deck(self, deck_type):
        if deck_type == "standard_deck":
            return StandardDeck()
        elif deck_type == "standard_deck_with_jokers":
            return StandardDeckWithJokers()
        elif deck_type == "canasta_deck":
            return JokerDeck()
        elif deck_type == "empty_deck":
            return EmptyDeck()
        raise UnsupportedDeckType(f"{deck_type} is not supported")

    def _get_deck_for_picking(self, source: Union[list, StandardDeck]) -> StandardDeck:
        if isinstance(source, list):
            # We have a list not a deck, lets create a deck from `from_sequence`
            # and then pick cards from it
            deck = EmptyDeck()
            for card in source:
                deck.insert_card(card, force=True)
        elif StandardDeck in type.mro(source.__class__):
            deck = source
        else:
            raise BadSource("This sequence can't be used for picking card")
        return deck

    def command_pick_random_cards(self, count: int, from_sequence: int) -> list[Card]:
        source = self.sequence_results[from_sequence]
        deck = self._get_deck_for_picking(source)
        return deck.pick_random_cards(count)

    def command_pick_specific_cards(self, cards: Iterable[Card], from_sequence: int):
        source = self.sequence_results[from_sequence]
        deck = self._get_deck_for_picking(source)
        picked_cards = []
        for card in cards:
            card = Card(value=card["value"], suit=card["suit"])
            picked_cards.append(deck.pick_card(card))
        return picked_cards

    def command_shuffle(self, sequence: int) -> StandardDeck:
        source = self.sequence_results[sequence]
        deck = self._get_deck_for_picking(source)
        deck.shuffle()
        return deck
