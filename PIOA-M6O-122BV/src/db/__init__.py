from .backend.memory import InMemoryDB
from .backend.file_database import FileDatabase

MemoryDatabase = InMemoryDB

__all__ = ["InMemoryDB", "MemoryDatabase", "FileDatabase"]