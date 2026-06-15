import os
from .backend.memory import InMemoryDB
from typing import List, Tuple, Dict, Any

class Tui:
    def __init__(self, db: InMemoryDB) -> None:
        self.db: InMemoryDB = db
        self.fields: List[str] = ["brand", "model", "year", "country"]

    def clear_screen(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self) -> None:
        print("=" * 60)
        print("База данных автомобилей")
        print("=" * 60)

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
            brand = record.get('brand', '')[:30]
            model = record.get('model', '')[:20]
            year = record.get('year', '')
            country = record.get('country', '')[:15]
            print(f"{record_id:<5} {brand:<20} {model:<20} {year:<6} {country:<15}")

    def get_car_data(self) -> Dict[str, Any]:
        print("\nВведите данные автомобиля:")

        brand = input("brand: ").strip()
        if not brand:
            raise ValueError("Введите данные повторно")

        model = input("model: ").strip()
        if not model:
            raise ValueError("Введите данные повторно")

        year = None
        while True:
            year_input = input("Год производства: ").strip()
            if not year_input:
                break
            try:
                year = int(year_input)
                if year < 1900:
                    print("Год должен быть больше 1900")
                    continue
                break
            except ValueError:
                print("Год должен быть числом")

        country = input("country: ").strip()

        data = {
            "brand": brand,
            "model": model,
            "country": country,
        }

        if year is not None:
            data["year"] = year

        return data


    def add_record(self) -> None:
        try:
            data = self.get_car_data()
            record_id = self.db.add_record(data)
            print(f"\nМодель внесена с базу, ID: {record_id}")
        except ValueError as e:
            print(f"\nОшибка ввода: {e}")
        except Exception as e:
            print(f"\nОшибка добавления: {e}")

    def show_all(self) -> None:
        records = self.db.get_all_records()
        self.print_records(records)

# Реализация функции чтения записей с фильтрацией по полям

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
            records = self.db.filter_records(filters)
            self.print_records(records)
        except Exception as e:
            print(f"\nОшибка при поиске: {e}")


# Реализация функции обновления записей
    def update_record(self) -> None:
        try:
            record_id_input = input("\nДля обновления введите ID модели: ").strip()
            if not record_id_input.isdigit():
                print("ID должен быть числом")
                return

            record_id = int(record_id_input)
            current = self.db.get_record(record_id)
            print(f"\nТекущие данные: {current}")

            data = self.get_car_data()
            updated = self.db.update_record(record_id, data)
            print(f"\nМодель обновлена: {updated}")
        except KeyError as e:
            print(f"\nОшибка: {e}")
        except ValueError as e:
            print(f"\nОшибка ввода: {e}")
        except Exception as e:
            print(f"\nОшибка обновления: {e}")


# Реализация функции удаления записи
    def delete_record(self) -> None:
        try:
            record_id_input = input("\nВведите ID модели для удаления: ").strip()
            if not record_id_input.isdigit():
                print("ID должен быть числом")
                return

            record_id = int(record_id_input)
            deleted = self.db.delete_record(record_id)
            print(f"\n=Модель удалена: {deleted}")
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