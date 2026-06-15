from typing import Any, Dict, List, Tuple
from .errors import DuplicateIDError, InvalidYearError

class InMemoryDB:

    def __init__(self) -> None:
        self.records: Dict[int, Dict[str, Any]] = {}
        self.next_id: int = 1

    def add_record(self, data: Dict[str, Any]) -> int:
        if not isinstance(data, dict):
            raise TypeError("Данные должны быть словарем")
        
        if "brand" in data and not data["brand"]:
            raise ValueError("Поле brand не может быть пустым")
        if "model" in data and not data["model"]:
            raise ValueError("Поле model не может быть пустым")
        
        if "year" in data:
            year = data["year"]
            if not isinstance(year, int):
                raise TypeError("Год должен быть целым числом")
            if year < 1900 or year > 2026:
                raise InvalidYearError("Год производства должен быть между 1900 и 2026")
        
        if "id" in data:
            if data["id"] in self.records:
                raise DuplicateIDError(f"Запись с id={data['id']} уже существует.")

        record_id = self.next_id
        self.records[record_id] = data
        self.next_id += 1

        return record_id

    def get_all_records(self) -> List[Tuple[int, Dict[str, Any]]]:
        return list(self.records.items())

    def get_record(self, record_id: int) -> Dict[str, Any]:
        if record_id not in self.records:
            raise KeyError(f"Запись с ID {record_id} не найдена")

        return self.records[record_id]

    def filter_records(self, filters: Dict[str, Any]) -> List[Tuple[int, Dict[str, Any]]]:
        if not isinstance(filters, dict):
            raise TypeError("Фильтры должны быть словарем")

        result = []

        for record_id, record in self.records.items():
            match = True

            for key, value in filters.items():
                if key not in record or record[key] != value:
                    match = False
                    break

            if match:
                result.append((record_id, record))

        return result

    def update_record(self, record_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        if record_id not in self.records:
            raise KeyError(f"Запись с ID {record_id} не найдена")
        
        if "year" in data:
            year = data["year"]
            if not isinstance(year, int):
                raise TypeError("Год должен быть целым числом")
            if year < 1900 or year > 2026:
                raise InvalidYearError("Год производства должен быть между 1900 и 2026")
        
        if "brand" in data and not data["brand"]:
            raise ValueError("Поле brand не может быть пустым")
        if "model" in data and not data["model"]:
            raise ValueError("Поле model не может быть пустым")

        self.records[record_id].update(data)

        return self.records[record_id]

    def delete_record(self, record_id: int) -> Dict[str, Any]:
        if record_id not in self.records:
            raise KeyError(f"Запись с ID {record_id} не найдена")

        return self.records.pop(record_id)
