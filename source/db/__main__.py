from .backend.memory import InMemoryDB
from .tui import Tui

def main() -> None:
    try:
        db = InMemoryDB()
        ui = Tui(db)
        ui.run()
    except KeyboardInterrupt:
        print("\n\nРабота программы прервана")
    except Exception as e:
        print(f"\nКритическая ошибка: {e}")

if __name__ == "__main__":
    main()
