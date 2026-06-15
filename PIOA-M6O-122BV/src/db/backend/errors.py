
class CarTableError(Exception):
    """Базовый класс для ошибок, связанных с таблицей Student."""
    pass

class InvalidYearError(CarTableError):
    """Ошибка, возникающая при попытке создать запись с некорректным возрастом."""
    pass

class DuplicateIDError(CarTableError):
    """Ошибка, возникающая при попытке создать запись с уже существующим идентификатором."""
    pass