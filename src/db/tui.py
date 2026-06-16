import os
from typing import List, Tuple, Dict, Any

from .backend.memory import InMemoryDB
from .backend.file_database import FileDatabase


class Tui:
    def __init__(self, db: InMemoryDB | FileDatabase) -> None:
        self.db: InMemoryDB | FileDatabase = db
        self.fields: List[str] = ["brand", "model", "year", "country"]
        
        #Создание таблицы cars при запуске
        if hasattr(self.db, 'create_table'):
            try:
                self.db.create_table("cars", tuple(self.fields))
            except Exception:
                pass

    def clear_screen(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self) -> None:
        print("=" * 60)
        print("База данных автомобилей")
        print("=" * 60)

        if hasattr(self.db, 'directory'):
            print(f"Тип хранилища: Файловая (data/)")
        else:
            print(f"Тип хранилища: In-memory")

    def print_menu(self) -> None:
        print("\nМеню:")
        print("1. Добавить модель")
        print("2. Показать модели")
        print("3. Найти модель")
        print("4. Обновить модель")
        print("5. Удалить модель")
        print("6. Выход")

    def print_records(self, records: List[Tuple[int, Dict[str, Any]]]) -> None:
        if not records:
            print("\nНет записей")
            return

        print(f"\n{'ID':<5} {'brand':<20} {'model':<20} {'year':<6} {'country':<15}")
        print("-" * 70)

        for record_id, record in records:
            brand = record.get('brand', '')[:20]
            model = record.get('model', '')[:20]
            year = record.get('year', '')
            country = record.get('country', '')[:15]
            print(f"{record_id:<5} {brand:<20} {model:<20} {year:<6} {country:<15}")

    def get_car_data(self, is_update: bool = False) -> Dict[str, Any]:
        if not is_update:
            print("\nВведите данные автомобиля:")

        brand = input("brand: ").strip()
        if not brand and not is_update:
            raise ValueError("Поле brand обязательно для заполнения")

        model = input("model: ").strip()
        if not model and not is_update:
            raise ValueError("Поле model обязательно для заполнения")

        year = None
        year_input = input("Год производства: ").strip()
        if year_input:
            try:
                year = int(year_input)
                if year < 1900:
                    print("Год должен быть больше 1900")
                    year = None
            except ValueError:
                print("Год должен быть числом")

        country = input("country: ").strip()

        data = {}
        if brand:
            data["brand"] = brand
        if model:
            data["model"] = model
        if year is not None:
            data["year"] = year
        if country:
            data["country"] = country

        return data

    def add_record(self) -> None:
        try:
            data = self.get_car_data(is_update=False)
            if not data:
                print("\nОшибка: нет данных для добавления")
                return
            
            if hasattr(self.db, 'insert_record'):
                self.db.insert_record("cars", data)
                print(f"\nМодель внесена в базу данных")
            else:

                record_id = self.db.add_record(data)
                print(f"\nМодель внесена в базу, ID: {record_id}")
        except ValueError as e:
            print(f"\nОшибка ввода: {e}")
        except Exception as e:
            print(f"\nОшибка добавления: {e}")

    def show_all(self) -> None:
        try:

            if hasattr(self.db, 'select_records'):
                records_data = self.db.select_records("cars")

                records = [(i + 1, r) for i, r in enumerate(records_data)]
            else:

                records = self.db.get_all_records()
            self.print_records(records)
        except Exception as e:
            print(f"\nОшибка получения записей: {e}")

    def get_filters(self) -> Dict[str, Any]:
        filters = {}
        print("\nВведите критерии поиска (оставьте пустым для пропуска):")

        for field in self.fields:
            value = input(f"{field}: ").strip()
            if value:
                if field == "year":
                    try:
                        filters[field] = int(value)
                    except ValueError:
                        print(f"{field} должен быть числом, пропуск фильтра")
                else:
                    filters[field] = value
        return filters

    def filter_records(self) -> None:
        try:
            filters = self.get_filters()
            if not filters:
                print("Не задано фильтров")
                return
            
            if hasattr(self.db, 'select_records'):
                records_data = self.db.select_records("cars", **filters)
                records = [(i + 1, r) for i, r in enumerate(records_data)]
            else:
                records = self.db.filter_records(filters)
            
            self.print_records(records)
        except Exception as e:
            print(f"\nОшибка при поиске: {e}")

    def update_record(self) -> None:
        try:
            if hasattr(self.db, 'select_records'):
                all_records = self.db.select_records("cars")
                if not all_records:
                    print("\nНет записей для обновления")
                    return
                
                print("\nДоступные записи:")
                for idx, record in enumerate(all_records, 1):
                    print(f"  {idx}. {record}")
                
                idx_input = input("\nВведите номер записи для обновления: ").strip()
                if not idx_input.isdigit():
                    print("Номер должен быть числом")
                    return
                
                idx = int(idx_input) - 1
                if idx < 0 or idx >= len(all_records):
                    print("Неверный номер записи")
                    return
                
                current = all_records[idx]
                print(f"\nТекущие данные: {current}")
                
                print("\nВведите новые данные (оставьте поле пустым, чтобы не менять):")
                new_data = {}
                
                brand = input(f"brand [{current.get('brand', '')}]: ").strip()
                if brand:
                    new_data["brand"] = brand
                
                model = input(f"model [{current.get('model', '')}]: ").strip()
                if model:
                    new_data["model"] = model
                
                year_input = input(f"Год производства [{current.get('year', '')}]: ").strip()
                if year_input:
                    try:
                        year = int(year_input)
                        if year >= 1900:
                            new_data["year"] = year
                    except ValueError:
                        print("Год должен быть числом")
                
                country = input(f"country [{current.get('country', '')}]: ").strip()
                if country:
                    new_data["country"] = country
                
                if not new_data:
                    print("Нет данных для обновления")
                    return
                
                current.update(new_data)
                all_records[idx] = current
                
                if hasattr(self.db, 'clear_table'):
                    self.db.clear_table("cars")
                else:
                    try:
                        self.db.create_table("cars", tuple(self.fields))
                    except Exception:
                        pass
                
                for record in all_records:
                    record_copy = {k: v for k, v in record.items() if k != 'id'}
                    self.db.insert_record("cars", record_copy)
                
                print(f"\nМодель обновлена: {current}")
            else:

                record_id_input = input("\nДля обновления введите ID модели: ").strip()
                if not record_id_input.isdigit():
                    print("ID должен быть числом")
                    return

                record_id = int(record_id_input)
                current = self.db.get_record(record_id)
                print(f"\nТекущие данные: {current}")

                data = self.get_car_data(is_update=True)
                updated = self.db.update_record(record_id, data)
                print(f"\nМодель обновлена: {updated}")
        except KeyError as e:
            print(f"\nОшибка: {e}")
        except ValueError as e:
            print(f"\nОшибка ввода: {e}")
        except Exception as e:
            print(f"\nОшибка обновления: {e}")

    def delete_record(self) -> None:
        try:
            if hasattr(self.db, 'select_records'):
                all_records = self.db.select_records("cars")
                if not all_records:
                    print("\nНет записей для удаления")
                    return
                
                print("\nДоступные записи:")
                for idx, record in enumerate(all_records, 1):
                    print(f"  {idx}. {record}")
                
                idx_input = input("\nВведите номер записи для удаления: ").strip()
                if not idx_input.isdigit():
                    print("Номер должен быть числом")
                    return
                
                idx = int(idx_input) - 1
                if idx < 0 or idx >= len(all_records):
                    print("Неверный номер записи")
                    return
                
                deleted = all_records.pop(idx)
                
                if hasattr(self.db, 'clear_table'):
                    self.db.clear_table("cars")
                else:
                    try:
                        self.db.create_table("cars", tuple(self.fields))
                    except Exception:
                        pass  
                
                for record in all_records:
                    record_copy = {k: v for k, v in record.items() if k != 'id'}
                    self.db.insert_record("cars", record_copy)
                
                print(f"\nМодель удалена: {deleted}")
            else:
                record_id_input = input("\nВведите ID модели для удаления: ").strip()
                if not record_id_input.isdigit():
                    print("ID должен быть числом")
                    return

                record_id = int(record_id_input)
                deleted = self.db.delete_record(record_id)
                print(f"\nМодель удалена: {deleted}")
        except KeyError as e:
            print(f"\nОшибка: {e}")
        except Exception as e:
            print(f"\nОшибка удаления: {e}")

    def run(self) -> None:
        while True:
            self.clear_screen()
            self.print_header()
            self.print_menu()

            choice = input("\nВыбор действия: ").strip()

            if choice == '1':
                self.add_record()
            elif choice == '2':
                self.show_all()
            elif choice == '3':
                self.filter_records()
            elif choice == '4':
                self.update_record()
            elif choice == '5':
                self.delete_record()
            elif choice == '6':
                print("\nВыход выполнен")
                break
            else:
                print("\nОшибка")

            input("\nНажмите Enter для продолжения...")