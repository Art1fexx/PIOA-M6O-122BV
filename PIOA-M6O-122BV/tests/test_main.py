import unittest
from unittest.mock import patch

class TestDbMain(unittest.TestCase):
    
    @patch("src.db.__main__.run")
    def test_main_calls_run(self, mock_run):
        from src.db.__main__ import main
        main()
        mock_run.assert_called_once()
    
    @patch("src.db.__main__.run")
    def test_run_is_callable(self, mock_run):
        from src.db.__main__ import run
        self.assertTrue(callable(run))