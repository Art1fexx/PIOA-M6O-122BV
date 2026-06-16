import pytest
from src.db.backend.memory import InMemoryDB


class TestInMemoryDB:

    def setup_method(self):
        self.db = InMemoryDB()

    def test_add_record_success(self):
        data = {"brand": "Toyota", "model": "Camry", "year": 2020, "country": "Japan"}
        record_id = self.db.add_record(data)

        assert record_id == 1
        assert self.db.records[1] == data

    def test_add_record_with_invalid_data_type(self):
        with pytest.raises(TypeError, match="Данные должны быть словарем"):
            self.db.add_record("not a dict")

    def test_add_record_multiple_records(self):
        id1 = self.db.add_record({"brand": "Toyota", "model": "Camry"})
        id2 = self.db.add_record({"brand": "BMW", "model": "X5"})
        id3 = self.db.add_record({"brand": "Ford", "model": "Focus"})

        assert id1 == 1
        assert id2 == 2
        assert id3 == 3
        assert len(self.db.records) == 3

    def test_get_all_records_empty(self):
        records = self.db.get_all_records()
        assert records == []

    def test_get_all_records_with_data(self):
        self.db.add_record({"brand": "Toyota", "model": "Camry"})
        self.db.add_record({"brand": "BMW", "model": "X5"})

        records = self.db.get_all_records()
        assert len(records) == 2
        assert records[0][0] == 1
        assert records[1][0] == 2

    def test_get_record_success(self):
        self.db.add_record({"brand": "Toyota", "model": "Camry", "year": 2020, "country": "Japan"})
        record = self.db.get_record(1)

        assert record == {"brand": "Toyota", "model": "Camry", "year": 2020, "country": "Japan"}

    def test_get_record_not_found(self):
        with pytest.raises(KeyError, match="Запись с ID 999 не найдена"):
            self.db.get_record(999)

    def test_filter_records_success_single_filter(self):
        self.db.add_record({"brand": "Toyota", "model": "Camry", "year": 2020, "country": "Japan"})
        self.db.add_record({"brand": "BMW", "model": "X5", "year": 2022, "country": "Germany"})
        self.db.add_record({"brand": "Toyota", "model": "Corolla", "year": 2021, "country": "Japan"})

        result = self.db.filter_records({"brand": "Toyota"})

        assert len(result) == 2

    def test_filter_records_success_multiple_filters(self):
        self.db.add_record({"brand": "Toyota", "model": "Camry", "year": 2020, "country": "Japan"})
        self.db.add_record({"brand": "Toyota", "model": "Corolla", "year": 2021, "country": "Japan"})
        self.db.add_record({"brand": "BMW", "model": "X5", "year": 2022, "country": "Germany"})

        result = self.db.filter_records({"brand": "Toyota", "year": 2021})

        assert len(result) == 1
        assert result[0][1]["model"] == "Corolla"

    def test_filter_records_no_match(self):
        self.db.add_record({"brand": "Toyota", "model": "Camry"})
        result = self.db.filter_records({"brand": "Nonexistent"})

        assert result == []

    def test_filter_records_empty_filters(self):
        self.db.add_record({"brand": "Toyota"})
        result = self.db.filter_records({})

        assert len(result) == 1

    def test_filter_records_invalid_filters_type(self):
        with pytest.raises(TypeError, match="Фильтры должны быть словарем"):
            self.db.filter_records("not a dict")

    def test_update_record_success(self):
        self.db.add_record({"brand": "Toyota", "model": "Camry", "year": 2020})
        updated = self.db.update_record(1, {"year": 2023})

        assert updated == {"brand": "Toyota", "model": "Camry", "year": 2023}

    def test_update_record_not_found(self):
        with pytest.raises(KeyError, match="Запись с ID 999 не найдена"):
            self.db.update_record(999, {"year": 2023})

    def test_delete_record_success(self):
        self.db.add_record({"brand": "Toyota", "model": "Camry"})
        deleted = self.db.delete_record(1)

        assert deleted == {"brand": "Toyota", "model": "Camry"}
        assert 1 not in self.db.records
        assert len(self.db.records) == 0

    def test_delete_record_not_found(self):
        with pytest.raises(KeyError, match="Запись с ID 999 не найдена"):
            self.db.delete_record(999)

    def test_update_record_partial_update(self):
        self.db.add_record({"brand": "Toyota", "model": "Camry", "year": 2020, "country": "Japan"})
        self.db.update_record(1, {"year": 2023, "country": "USA"})

        record = self.db.get_record(1)
        assert record["brand"] == "Toyota"
        assert record["model"] == "Camry"
        assert record["year"] == 2023
        assert record["country"] == "USA"

    def test_filter_records_case_sensitive(self):
        self.db.add_record({"brand": "toyota", "model": "Camry"})
        self.db.add_record({"brand": "Toyota", "model": "Corolla"})

        result = self.db.filter_records({"brand": "Toyota"})

        assert len(result) == 1
        assert result[0][1]["model"] == "Corolla"