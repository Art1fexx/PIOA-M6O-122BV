import pytest
import json
from pathlib import Path
from src.db.backend.file_database import FileDatabase
from src.db.backend.table import Table
from src.db.backend.errors import TableNotFoundError, InvalidStorageDataError


@pytest.fixture
def db(tmp_path):
    return FileDatabase(str(tmp_path))


@pytest.fixture
def setup_cars_table(db):
    columns = ("brand", "model", "year", "country")
    db.create_table("cars", columns)
    return db


class TestFileDatabase:
    def test_create_table(self, db):
        columns = ("brand", "model", "year")
        db.create_table("cars", columns)

        assert db._table_exists("cars")
        table = db._load_table("cars")
        assert table.columns == columns
        assert table.records == []

    def test_create_table_already_exists(self, db):
        db.create_table("cars", ("brand", "model"))
        with pytest.raises(Exception): 
            db.create_table("cars", ("brand", "model"))

    def test_insert_record(self, setup_cars_table):
        db = setup_cars_table
        record = {"brand": "Toyota", "model": "Camry", "year": 2020, "country": "Japan"}
        db.insert_record("cars", record)

        table = db._load_table("cars")
        assert len(table.records) == 1
        assert table.records[0]["brand"] == "Toyota"
        assert table.records[0]["model"] == "Camry"

    def test_insert_record_missing_column(self, setup_cars_table):
        db = setup_cars_table
        record = {"brand": "Toyota", "model": "Camry"} 
        with pytest.raises(Exception): 
            db.insert_record("cars", record)

    def test_select_records_all(self, setup_cars_table):
        db = setup_cars_table
        db.insert_record("cars", {"brand": "Toyota", "model": "Camry", "year": 2020, "country": "Japan"})
        db.insert_record("cars", {"brand": "Honda", "model": "Civic", "year": 2019, "country": "Japan"})

        records = db.select_records("cars")
        assert len(records) == 2

    def test_select_records_with_filter(self, setup_cars_table):
        db = setup_cars_table
        db.insert_record("cars", {"brand": "Toyota", "model": "Camry", "year": 2020, "country": "Japan"})
        db.insert_record("cars", {"brand": "Honda", "model": "Civic", "year": 2019, "country": "Japan"})
        db.insert_record("cars", {"brand": "BMW", "model": "X5", "year": 2021, "country": "Germany"})

        records = db.select_records("cars", country="Japan")
        assert len(records) == 2

        records = db.select_records("cars", brand="Toyota", year=2020)
        assert len(records) == 1
        assert records[0]["model"] == "Camry"

    def test_select_records_no_match(self, setup_cars_table):
        db = setup_cars_table
        db.insert_record("cars", {"brand": "Toyota", "model": "Camry", "year": 2020, "country": "Japan"})

        records = db.select_records("cars", brand="Ferrari")
        assert records == []

    def test_table_not_found(self, db):
        with pytest.raises(TableNotFoundError):
            db.select_records("nonexistent")

    def test_persistence(self, tmp_path):
        db1 = FileDatabase(str(tmp_path))
        db1.create_table("cars", ("brand", "model", "year", "country"))
        db1.insert_record("cars", {"brand": "Toyota", "model": "Camry", "year": 2020, "country": "Japan"})

        db2 = FileDatabase(str(tmp_path))
        records = db2.select_records("cars")

        assert len(records) == 1
        assert records[0]["brand"] == "Toyota"
        assert records[0]["model"] == "Camry"

    def test_clear_table(self, setup_cars_table):
        db = setup_cars_table
        db.insert_record("cars", {"brand": "Toyota", "model": "Camry", "year": 2020, "country": "Japan"})
        db.insert_record("cars", {"brand": "Honda", "model": "Civic", "year": 2019, "country": "Japan"})

        db.clear_table("cars")

        records = db.select_records("cars")
        assert records == []
        table = db._load_table("cars")
        assert table.columns == ("brand", "model", "year", "country")

    def test_update_record_via_clear_and_reinsert(self, setup_cars_table):
        db = setup_cars_table
        db.insert_record("cars", {"brand": "Toyota", "model": "Camry", "year": 2020, "country": "Japan"})
        db.insert_record("cars", {"brand": "Honda", "model": "Civic", "year": 2019, "country": "Japan"})

        all_records = db.select_records("cars")
        all_records[0]["year"] = 2021
        db.clear_table("cars")
        for rec in all_records:
            db.insert_record("cars", rec)

        updated = db.select_records("cars", brand="Toyota")
        assert updated[0]["year"] == 2021

    def test_delete_record_via_clear_and_reinsert(self, setup_cars_table):
        db = setup_cars_table
        db.insert_record("cars", {"brand": "Toyota", "model": "Camry", "year": 2020, "country": "Japan"})
        db.insert_record("cars", {"brand": "Honda", "model": "Civic", "year": 2019, "country": "Japan"})

        all_records = db.select_records("cars")
        all_records.pop(0) 
        db.clear_table("cars")
        for rec in all_records:
            db.insert_record("cars", rec)

        remaining = db.select_records("cars")
        assert len(remaining) == 1
        assert remaining[0]["brand"] == "Honda"

    def test_invalid_json_handling(self, tmp_path):
        """Повреждённый JSON вызывает InvalidStorageDataError."""
        db = FileDatabase(str(tmp_path))
        db.create_table("cars", ("brand", "model"))

        # Поведение программы при повреждении файла .json
        table_path = tmp_path / "cars.json"
        with open(table_path, "w") as f:
            f.write("{ invalid json")

        db2 = FileDatabase(str(tmp_path))
        with pytest.raises(InvalidStorageDataError):
            db2.select_records("cars")