from typing import Any, Dict, List, Tuple
from datetime import datetime
from .errors import DuplicateIDError, InvalidYearError


class InMemoryDB:
    # База данных, работающая в оперативной памяти

    def __init__(self) -> None:
        self.records: Dict[int, Dict[str, Any]] = {}
        self.next_id: int = 1
        
        self.tables: Dict[str, Dict[int, Dict[str, Any]]] = {}
        self.next_table_ids: Dict[str, int] = {}

    def add_record(self, data: Dict[str, Any]) -> int:
        if not isinstance(data, dict):
            raise TypeError("Данные должны быть словарем")
        
        if "brand" in data and not data["brand"]:
            raise ValueError("Поле brand не может быть пустым")
        if "model" in data and not data["model"]:
            raise ValueError("Поле model не может быть пустым")
        
        current_year = datetime.now().year
        if "year" in data:
            year = data["year"]
            if not isinstance(year, int):
                raise TypeError("Год должен быть целым числом")
            if year < 1900 or year > current_year:
                raise InvalidYearError(f"Год производства должен быть между 1900 и {current_year}")
        
        if "id" in data:
            if data["id"] in self.records:
                raise DuplicateIDError(f"Запись с id={data['id']} уже существует.")

        record_id = self.next_id
        self.records[record_id] = data
        self.next_id += 1
        
        if "cars" not in self.tables:
            self.tables["cars"] = {}
            self.next_table_ids["cars"] = 1
        self.tables["cars"][record_id] = data
        if record_id >= self.next_table_ids["cars"]:
            self.next_table_ids["cars"] = record_id + 1

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
        
        current_year = datetime.now().year
        if "year" in data:
            year = data["year"]
            if not isinstance(year, int):
                raise TypeError("Год должен быть целым числом")
            if year < 1900 or year > current_year:
                raise InvalidYearError(f"Год производства должен быть между 1900 и {current_year}")
        
        if "brand" in data and not data["brand"]:
            raise ValueError("Поле brand не может быть пустым")
        if "model" in data and not data["model"]:
            raise ValueError("Поле model не может быть пустым")

        self.records[record_id].update(data)
        
        if "cars" in self.tables and record_id in self.tables["cars"]:
            self.tables["cars"][record_id].update(data)

        return self.records[record_id]

    def delete_record(self, record_id: int) -> Dict[str, Any]:
        if record_id not in self.records:
            raise KeyError(f"Запись с ID {record_id} не найдена")
        
        if "cars" in self.tables and record_id in self.tables["cars"]:
            del self.tables["cars"][record_id]

        return self.records.pop(record_id)

    #Совместимость с file_database 
    def create_table(self, table_name: str, columns: tuple) -> None:
        """Создаёт новую таблицу (для совместимости с FileDatabase)."""
        if table_name in self.tables:
            from .errors import TableAlreadyExistsError
            raise TableAlreadyExistsError(f"Таблица '{table_name}' уже существует.")
        self.tables[table_name] = {}
        self.next_table_ids[table_name] = 1

    def insert_record(self, table_name: str, record: Dict[str, Any]) -> None:
        """Добавляет запись в таблицу (для совместимости с FileDatabase)."""
        if table_name not in self.tables:
            from .errors import TableNotFoundError
            raise TableNotFoundError(f"Таблица '{table_name}' не существует.")
        
        if "id" in record:
            del record["id"]
        
        record_id = self.next_table_ids[table_name]
        self.tables[table_name][record_id] = record
        self.next_table_ids[table_name] += 1

    def select_records(self, table_name: str, **filters) -> List[Dict[str, Any]]:
        """Возвращает записи, удовлетворяющие фильтрам."""
        if table_name not in self.tables:
            from .errors import TableNotFoundError
            raise TableNotFoundError(f"Таблица '{table_name}' не существует.")
        
        records = self.tables[table_name]
        
        if not filters:
            return [record.copy() for record in records.values()]
        
        result = []
        for record_id, record in records.items():
            match = True
            for key, value in filters.items():
                if key not in record or record[key] != value:
                    match = False
                    break
            if match:
                result.append(record.copy())
        return result
    
    def clear_table(self, table_name: str) -> None:
        if table_name in self.tables:
            self.tables[table_name] = {}
            self.next_table_ids[table_name] = 1


# Обратная совместимость     
MemoryDatabase = InMemoryDB