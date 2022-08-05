from typing import Union, Iterable

from .exceptions import (
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
