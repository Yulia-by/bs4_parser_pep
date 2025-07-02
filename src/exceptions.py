class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""


class NotFoundException(Exception):
    """Вызывается, когда список с версиями Python не найден."""
    def __init__(self, message='Ничего не нашлось'):
        self.message = message
        super().__init__(self.message)
