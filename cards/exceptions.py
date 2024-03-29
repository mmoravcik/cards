class DeckFullException(Exception):
    pass


class NotEnoughCardsException(Exception):
    pass


class IncorrectDeckException(Exception):
    pass


class CardIsNotInTheDeck(Exception):
    pass


class UnsupportedAction(Exception):
    pass


class UnsupportedDeckType(Exception):
    pass


class UnsupportedCommand(Exception):
    pass


class BadSource(Exception):
    pass
