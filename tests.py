#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest
import sqlite3
from pathlib import Path
from ind_21 import create_db, add_human, select_all, select_zz


# Test case – это элементарная единица тестирования
class IndTests(unittest.TestCase):
    # Метод действует на уровне класса, т.е. выполняется
    # перед запуском тестов класса.
    @classmethod
    def setUpClass(cls):
        """Set up for class"""

        print("setUpClass")
        print("==========")

    # Запускается после выполнения всех методов класса
    @classmethod
    def tearDownClass(cls):
        """Tear down for class"""
        print("==========")
        print("tearDownClass")

    # Метод вызывается перед запуском теста. Как правило,
    # используется для подготовки окружения для теста.
    def setUp(self):
        """Set up for test"""
        print("Set up for [" + self.shortDescription() + "]")
        print("Creating the test DB...")

    # Метод вызывается после завершения работы теста.
    # Используется для “приборки” за тестом.
    def tearDown(self):
        """Tear down for test"""
        print("Tear down for [" + self.shortDescription() + "]")
        print("The test DB has been deleted")

    def test_create_db(self):
        """ Checking the database creation."""
        database_path = "test.db"
        if Path(database_path).exists():
            Path(database_path).unlink()

        create_db(database_path)
        self.assertTrue(Path(database_path).is_file())
        Path(database_path).unlink()

    def test_add_human(self):
        """ Checking the addition of a record about dates and zz."""
        database_path = "test.db"
        create_db(database_path)
        add_human(database_path, "Иванов Иван", "овен", "2001.03.21")
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM dates
            """
        )
        row = cursor.fetchone()
        self.assertEqual(row, (1, "овен", 1, "2001.03.21"))
        conn.close()
        Path(database_path).unlink()

    def test_select_all(self):
        """ Checking the selection of the entire list """
        database_path = "test.db"
        create_db(database_path)
        add_human(database_path, "Иванов Иван", "овен", "2001.03.21")
        add_human(database_path, "Петров Владимир", "лев", "2005.08.16")

        r_output = [
            {'name': "Иванов Иван", 'zodiac_sign': "овен", 'birth': "2001.03.21"},
            {'name': "Петров Владимир", 'zodiac_sign': "лев", 'birth': "2005.08.16"},
        ]
        self.assertEqual(select_all(database_path), r_output)
        Path(database_path).unlink()

    def test_select_zz(self):
        """ Checking the selection by zodiac sign """
        database_path = "test.db"
        create_db(database_path)
        add_human(database_path, "Иванов Иван", "овен", "2001.03.21")
        add_human(database_path, "Петров Владимир", "лев", "2005.08.16")
        r_output = [
            {'name': "Иванов Иван", 'zodiac_sign': "овен", 'birth': "2001.03.21"},
        ]
        self.assertEqual(select_zz(database_path, "овен"), r_output)
        Path(database_path).unlink()
