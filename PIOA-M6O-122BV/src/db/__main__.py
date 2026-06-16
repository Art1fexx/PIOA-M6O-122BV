from .backend.memory import InMemoryDB
from .backend.file_database import FileDatabase
from .tui import Tui


def choose_database():
    print("=" * 50)
    print("Система управления базой данных")
    print("=" * 50)
    print("\nВыберите тип хранения данных:")
    print("1. In-memory (Оперативная память)")
    print("2. File-based (Долговременная память)")
    
    while True:
        choice = input("\nВыбор: ").strip()
        if choice == "1":
            print("\nВыбор in-memory базы данных")
            return InMemoryDB()
        elif choice == "2":
            print("\nВыбор файловой база данных")
            print("Данные будут сохранены в каталог data")
            return FileDatabase()
        else:
            print("Неверный ввод. Введите 1 или 2.")


def run() -> None:
    db = choose_database()
    ui = Tui(db)
    ui.run()


def main() -> None:
    try:
        run()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем")
    except Exception as e:
        print(f"\nОшибка: {e}")


if __name__ == "__main__":
    main()
