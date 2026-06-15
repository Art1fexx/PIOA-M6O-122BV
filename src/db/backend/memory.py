from typing import Any, Dict, List, Tuple

class InMemoryDB:

    def __init__(self) -> None:
        self.records: Dict[int, Dict[str, Any]] = {}
        self.next_id: int = 1

    def add_record(self, data: Dict[str, Any]) -> int:
        if not isinstance(data, dict):
            raise TypeError("Данные должны быть словарем")

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
            raise TypeError("Фильтр должны быть словарем")

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

        self.records[record_id].update(data)

        return self.records[record_id]

    def delete_record(self, record_id: int) -> Dict[str, Any]:
        if record_id not in self.records:
            raise KeyError(f"Запись с ID {record_id} не найдена")

        return self.records.pop(record_id)