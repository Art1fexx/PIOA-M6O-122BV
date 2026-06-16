import unittest
from unittest.mock import Mock, patch

from src.db.tui import Tui

class TestTui(unittest.TestCase):

    def setUp(self):
        self.db = Mock()
        self.tui = Tui(self.db)

    def test_get_car_data(self):
        cases = [
            (
                ["Toyota", "Camry", "2020", "Japan"],
                {
                    "brand": "Toyota",
                    "model": "Camry",
                    "year": 2020,
                    "country": "Japan",
                },
            ),
            (
                ["BMW", "X5", "", "Germany"],
                {
                    "brand": "BMW",
                    "model": "X5",
                    "country": "Germany",
                },
            ),
        ]

        for inputs, expected in cases:
            with self.subTest(inputs=inputs):
                with patch("builtins.input", side_effect=inputs):
                    result = self.tui.get_car_data()

                self.assertEqual(result, expected)

    def test_get_car_data_errors(self):
        cases = [
            [""],
            ["Toyota", ""],
        ]

        for inputs in cases:
            with self.subTest(inputs=inputs):
                with patch("builtins.input", side_effect=inputs):
                    with self.assertRaises(ValueError):
                        self.tui.get_car_data()

    def test_get_filters(self):
        with patch(
            "builtins.input",
            side_effect=[
                "Toyota",
                "Camry",
                "2020",
                "Japan",
            ],
        ):
            filters = self.tui.get_filters()

        self.assertEqual(
            filters,
            {
                "brand": "Toyota",
                "model": "Camry",
                "year": 2020,
                "country": "Japan",
            },
        )

    def test_add_record(self):
        self.db.add_record.return_value = 1

        with patch.object(
            self.tui,
            "get_car_data",
            return_value={"brand": "Toyota"},
        ):
            self.tui.add_record()

        self.db.add_record.assert_called_once()

    def test_add_record_errors(self):
        with patch.object(
            self.tui,
            "get_car_data",
            side_effect=ValueError(),
        ):
            self.tui.add_record()

        self.db.add_record.side_effect = Exception()

        with patch.object(
            self.tui,
            "get_car_data",
            return_value={"brand": "Toyota"},
        ):
            self.tui.add_record()

    def test_show_all(self):
        self.db.get_all_records.return_value = []

        with patch.object(
            self.tui,
            "print_records",
        ) as mock_print:
            self.tui.show_all()

        mock_print.assert_called_once()

    def test_filter_records(self):
        self.db.filter_records.return_value = []

        with patch.object(
            self.tui,
            "get_filters",
            return_value={"brand": "Toyota"},
        ):
            self.tui.filter_records()

        self.db.filter_records.assert_called_once()

    def test_filter_records_empty(self):
        with patch.object(
            self.tui,
            "get_filters",
            return_value={},
        ):
            self.tui.filter_records()

    def test_filter_records_exception(self):
        self.db.filter_records.side_effect = Exception()

        with patch.object(
            self.tui,
            "get_filters",
            return_value={"brand": "Toyota"},
        ):
            self.tui.filter_records()

    def test_update_record(self):
        self.db.get_record.return_value = {}
        self.db.update_record.return_value = {}

        with patch(
            "builtins.input",
            side_effect=["1"],
        ):
            with patch.object(
                self.tui,
                "get_car_data",
                return_value={"brand": "Toyota"},
            ):
                self.tui.update_record()

        self.db.update_record.assert_called_once()

    def test_update_record_errors(self):

        self.db.get_record.side_effect = KeyError()

        with patch(
            "builtins.input",
            side_effect=["1"],
        ):
            self.tui.update_record()

        self.db.get_record.side_effect = None
        self.db.get_record.return_value = {}

        with patch(
            "builtins.input",
            side_effect=["1"],
        ):
            with patch.object(
                self.tui,
                "get_car_data",
                side_effect=ValueError(),
            ):
                self.tui.update_record()

        self.db.update_record.side_effect = Exception()

        with patch(
            "builtins.input",
            side_effect=["1"],
        ):
            with patch.object(
                self.tui,
                "get_car_data",
                return_value={"brand": "Toyota"},
            ):
                self.tui.update_record()

    def test_delete_record(self):
        self.db.delete_record.return_value = {}

        with patch(
            "builtins.input",
            side_effect=["1"],
        ):
            self.tui.delete_record()

        self.db.delete_record.assert_called_once_with(1)

    def test_delete_record_errors(self):

        self.db.delete_record.side_effect = KeyError()

        with patch(
            "builtins.input",
            side_effect=["1"],
        ):
            self.tui.delete_record()

        self.db.delete_record.side_effect = Exception()

        with patch(
            "builtins.input",
            side_effect=["1"],
        ):
            self.tui.delete_record()

    @patch("builtins.print")
    def test_print_methods(self, mock_print):
        self.tui.print_header()
        self.tui.print_menu()
        self.tui.print_records([])

        self.tui.print_records(
            [
                (
                    1,
                    {
                        "brand": "Toyota",
                        "model": "Camry",
                        "year": 2020,
                        "country": "Japan",
                    },
                )
            ]
        )

        self.assertTrue(mock_print.called)

    @patch("os.system")
    def test_clear_screen(self, mock_system):
        self.tui.clear_screen()
        mock_system.assert_called_once()

    def test_run(self):

        actions = [
            ("1", "add_record"),
            ("2", "show_all"),
            ("3", "filter_records"),
            ("4", "update_record"),
            ("5", "delete_record"),
        ]

        for choice, method in actions:
            with self.subTest(choice=choice):

                with patch.object(
                    self.tui,
                    method,
                ) as mock_method:

                    with patch(
                        "builtins.input",
                        side_effect=[choice, "", "6"],
                    ):
                        self.tui.run()

                    mock_method.assert_called_once()

    def test_run_invalid_choice(self):
        with patch(
            "builtins.input",
            side_effect=["999", "", "6"],
        ):
            self.tui.run()

