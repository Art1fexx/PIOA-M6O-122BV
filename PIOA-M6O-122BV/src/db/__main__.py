from .backend.memory import InMemoryDB
from .tui import Tui

def run() -> None:
    db = InMemoryDB()
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