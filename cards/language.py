from copy import copy

from .exceptions import UnsupportedAction, UnsupportedCommand
from .models import EmptyDeck, StandardDeck, StandardDeckWithJokers, JokerDeck, Card


class Language(object):
    deck = None
    sequence_results = {}
    current_sequence = None

    ACTIONS_AND_COMMANDS = {
        "start_with": ["standard_deck", "standard_deck_with_jokers", "canasta_deck", "empty_deck"],
        "shuffle": ["all_deck"],
        "reset": [],
        "pick": ["random_cards", "specific_cards"],
        "insert": ["specific_picked_card", "random_picked_cards"],
        "insert_force": ["specific_picked_card", "random_picked_cards", "specific_card", "random_card", "joker"],
        "compare_picked": ["all_match", "any_match", "order_match"]  # ["specific_cards", "suits", "values", "colour",  "picture_card", "number_card"],
    }

    def __init__(self, sequences):
        self.sequences = sequences

    def execute_sequence(self, action, command, **kwargs):
        if action not in self.ACTIONS_AND_COMMANDS.keys():
            raise UnsupportedAction()

        if command and command not in self.ACTIONS_AND_COMMANDS[action]:
            raise UnsupportedCommand()

        return getattr(self, 'action_' + action)(command, **kwargs)

    def execute(self):
        self.current_sequence = 1
        self.sequence_results = {}
        for sequence in self.sequences:
            self.sequence_results[self.current_sequence] = self.execute_sequence(
                action=sequence["action"],
                command=sequence.get("command"),
                **sequence.get('meta', {})
            )
            self.current_sequence += 1
        return self.sequence_results

    def action_compare_picked(self, command, conditions=None, colours=None, suits=None, cards=None, from_sequence=None, values=None, matches_required=1):
        if from_sequence is None:
            # We are comparing picked cards from a previous sequence by default
            from_sequence = self.current_sequence - 1

        # Make sure that removing elements from these array won't affect global scale
        suits = copy(suits)
        colours = copy(colours)
        cards = copy(cards)
        values = copy(values)
        if command == "any_match":
            matches = 0
            for card in self.sequence_results[from_sequence]:
                for condition in conditions or []:
                    if condition["type"] == "colours":
                        if card.colour in condition["values"]:
                            matches += 1
                    elif condition["type"] == "values":
                        if card.value in condition["values"]:
                            matches += 1
                    elif condition["type"] == "specific_cards":
                        for specific_card in condition["values"]:
                            _card = Card(value=specific_card["value"], suit=specific_card["suit"])
                            if card.is_the_same_card(_card):
                                matches += 1
                    elif condition["type"] == "suits":
                        if card.suit in condition["values"]:
                            matches += 1
            return matches_required <= matches
        elif command == "all_match":
            for cond in conditions or []:
                condition_values = copy(cond["values"])
                for card in self.sequence_results[from_sequence]:
                    if cond["type"] == "colours":
                        if card.colour not in condition_values:
                            return False
                        else:
                            condition_values.remove(card.colour)
                    elif cond["type"] == "values":
                        if card.value not in condition_values:
                            return False
                        else:
                            condition_values.remove(card.value)
                    elif cond["type"] == "specific_cards":
                        if card not in [Card(value=c["value"], suit=c["suit"]) for c in condition_values]:
                            return False
                        else:
                            condition_values.remove({"value": card.value, "suit": card.suit})
                    elif cond["type"] == "suits":
                        if card.suit not in condition_values:
                            return False
                        else:
                            condition_values.remove(card.suit)
            return True
        elif command == "order_match":
            for idx, card in enumerate(self.sequence_results[from_sequence]):
                if colours:
                    if card.colour != colours[idx]:
                        return False
                elif values:
                    if card.value != values[idx]:
                        return False
                elif cards:
                    if card != [Card(value=c["value"], suit=c["suit"]) for c in cards][idx]:
                        return False
                elif suits:
                    if card.suit != suits[idx]:
                        return False
            return True

    def action_start_with(self, command):
        if command == "standard_deck":
            self.deck = StandardDeck()
        elif command == "standard_deck_with_jokers":
            self.deck = StandardDeckWithJokers()
        elif command == "canasta_deck":
            self.deck = JokerDeck()
        elif command == "empty_deck":
            self.deck = EmptyDeck()
        return self.deck

    def action_pick(self, command, count=1, specific_cards=None):
        if command == "random_cards":
            picked_cards = self.deck.pick_random_cards(count)
        elif command == "specific_cards":
            picked_cards = []
            for card in specific_cards or []:
                picked_cards.append(self.deck.pick_card(card))
        return picked_cards