#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sqlite3
import typing as t
from pathlib import Path


def display_people(people_list: t.List[t.Dict[str, t.Any]]) -> None:
    if people_list:
        # Заголовок таблицы.
        line = (f'{"+" + "-" * 15 + "+" + "-" * 12 + "+"}'
                f'{"-" * 15 + "+"}')
        print(line)
        print(f"|{'Name' :^15}|{'Birth ' :^12}|{'Zodiac_sign ' :^15}|")
        print(line)

        # Вывести данные о всех людях.
        for idx, man in enumerate(people_list):
            print(
                f'|{man.get("name", "") :^15}'
                f'|{man.get("birth", "") :^12}'
                f'|{man.get("zodiac_sign", "") :^15}|'
            )
            print(line)
    else:
        print("Список пуст.")


def add_human(
        database_path: Path,
        name: str,
        zodiac_sign: str,
        birth: str
) -> None:
    """
    Добавить работника в базу данных.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT people_id FROM people WHERE people_title = ?
        """,
        (name,)
    )
    row = cursor.fetchone()

    if row is None:
        cursor.execute(
            """
            INSERT INTO people (people_title) VALUES (?)
            """,
            (name,)
        )
        zodiac_sign_id = cursor.lastrowid

    else:
        zodiac_sign_id = row[0]
    # Добавить информацию о новом работнике.
    cursor.execute(
        """
        INSERT INTO dates (zodiac_sign_name, people_id, birth_year)
        VALUES (?, ?, ?)
        """,
        (zodiac_sign, zodiac_sign_id, birth)
    )
    conn.commit()
    conn.close()


def create_db(database_path: Path) -> None:
    """
    Создать базу данных.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Создать таблицу с информацией о людях(ФИО).
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS people (
        people_id INTEGER PRIMARY KEY AUTOINCREMENT,
        people_title TEXT NOT NULL
        )
        """
    )
    # Создать таблицу с информацией о ЗЗ и ДР.
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS dates (
        zodiac_sign_id INTEGER PRIMARY KEY AUTOINCREMENT,
        zodiac_sign_name TEXT NOT NULL,
        people_id INTEGER NOT NULL,
        birth_year DATE NOT NULL,
        FOREIGN KEY(people_id) REFERENCES people(people_id)
        )
        """
    )
    conn.close()


def select_all(database_path: Path) -> t.List[t.Dict[str, t.Any]]:
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT people.people_title, dates.zodiac_sign_name, dates.birth_year
        FROM dates
        INNER JOIN people ON people.people_id = dates.people_id
        """
    )
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "name": row[0],
            "zodiac_sign": row[1],
            "birth": row[2],
        }
        for row in rows
    ]


def select_zz(
        database_path: Path, zz: str
) -> t.List[t.Dict[str, t.Any]]:
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT people.people_title, dates.zodiac_sign_name, dates.birth_year
        FROM dates
        INNER JOIN people ON people.people_id = dates.people_id
        WHERE dates.zodiac_sign_name == ?
        """,
        (zz,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "name": row[0],
            "zodiac_sign": row[1],
            "birth": row[2],
        }
        for row in rows
    ]


def main(command_line=None):
    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "--db",
        action="store",
        required=False,
        ###### !!!!!!!!!!!!!!!!! Path.home() / "workers.db"
        default=str(Path.cwd() / "Ind.db"),
        help="The database file name"
    )
    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("people")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    subparsers = parser.add_subparsers(dest="command")

    # Создать субпарсер для добавления людей.
    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new person"
    )
    add.add_argument(
        "-n",
        "--name",
        action="store",
        required=True,
        help="The person's name"
    )
    add.add_argument(
        "-z",
        "--zodiac_sign",
        action="store",
        help="The person's zodiac_sign"
    )
    add.add_argument(
        "-b",
        "--birth",
        action="store",
        required=True,
        help="The person's birth"
    )

    # Создать субпарсер для отображения всех людей.
    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all people"
    )

    # Создать субпарсер для выбора знака зодиака.
    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select person"
    )

    select.add_argument(
        "-S",
        "--zodiac_sign",
        action="store",
        required=True,
        help="The required zodiac_sign"
    )

    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)

    # Получить путь к файлу базы данных.
    db_path = Path(args.db)
    create_db(db_path)

    # Добавить работника.
    if args.command == "add":
        add_human(db_path, args.name, args.zodiac_sign, args.birth)

    # Отобразить всех работников.
    elif args.command == "display":
        display_people(select_all(db_path))

    # Выбрать требуемых работников.
    elif args.command == "select":
        display_people(select_zz(db_path, args.zodiac_sign))
        pass


if __name__ == '__main__':
    main()
