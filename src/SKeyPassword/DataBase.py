import sqlite3


def validator(args):
    if type(args) is str:
        return args.lower().title(),
    elif type(args) is int:
        return args,
    elif any(map(lambda x: type(x) == int, args)):
        return args
    return tuple(
        map(lambda x: x.strip().lower().title(), args[:3])
    ) + args[3:]


class DataBase:
    def __init__(self):
        self.con = sqlite3.connect("passwords.sqlite")

    def change_db(self, path):
        self.con = sqlite3.connect(path)

    def is_category(self, category):
        cur = self.con.cursor()
        return bool(cur.execute('''
                                SELECT id
                                FROM Passwords
                                WHERE app_type =
                                (SELECT id
                                FROM Types
                                WHERE type_name = ?)
                                ''', validator(category)).fetchall())

    def get_entry(self, id):
        cur = self.con.cursor()
        return cur.execute("""
                           SELECT
                           login, password,
                           app_name,
                           (SELECT type_name
                           FROM Types
                           WHERE app_type = id)
                           FROM Passwords
                           WHERE id = ?
                           """, validator(id)
                           ).fetchone()

    def get_apps(self) -> list[str]:
        """Загружает и возвращает список приложений"""
        cur = self.con.cursor()
        return list(map(lambda x: x[0],
                        cur.execute('''
                                    SELECT DISTINCT app_name
                                    FROM Passwords
                                    ''').fetchall()))

    def get_categories(self) -> list[str]:
        """Загружает и возвращает список категорий"""
        cur = self.con.cursor()
        return list(map(lambda x: x[0],
                        cur.execute('''
                                    SELECT type_name
                                    FROM Types
                                    ''').fetchall()))

    def get_category(self, id):
        cur = self.con.cursor()
        return cur.execute('''
                           SELECT type_name
                           FROM Types
                           WHERE id =
                           (SELECT app_type
                           FROM Passwords
                           WHERE id = ?)
                           ''', validator(id)).fetchone()

    def load_id(self, filter='', condition='') -> tuple[int]:
        """Загружает и возвращает список id записей"""
        cur = self.con.cursor()
        if filter == "Категории" and condition:
            return tuple(map(lambda x: int(x[0]),
                             cur.execute('''
                                         SELECT id
                                         FROM Passwords
                                         WHERE app_type =
                                         (SELECT id FROM Types
                                         WHERE type_name = ?)
                                         ''',
                                         validator(condition)).fetchall()))
        elif filter == "Приложения" and condition:
            return tuple(map(lambda x: int(x[0]),
                             cur.execute('''
                                         SELECT id
                                         FROM Passwords
                                         WHERE app_name = ?
                                         ''',
                                         validator(condition)).fetchall()))
        return tuple(map(lambda x: int(x[0]),
                         cur.execute('''
                                     SELECT id
                                     FROM Passwords
                                     ''').fetchall()))

    def add(self, args):
        cur = self.con.cursor()
        self.add_category(args[0])
        cur.execute("""
                    INSERT INTO
                    Passwords(app_type, app_name, login, password)
                    VALUES((SELECT id FROM Types WHERE
                    type_name = ?), ?, ?, ?)
                    """, validator(args))
        self.con.commit()

    def add_category(self, category):
        """Проверяет есть ли категория в базе данных
                        и если нет, добавляет её туда"""
        cur = self.con.cursor()
        if not self.is_category(category):
            cur.execute('''
                        INSERT INTO Types(type_name)
                        VALUES(?)
                        ''', validator(category))
            self.con.commit()

    def overwrite(self, id, args):
        cur = self.con.cursor()
        old_category = self.get_category(id)
        self.add_category(args[0])
        cur.execute("""
                    UPDATE Passwords
                    SET app_type =
                    (SELECT id FROM Types
                    WHERE type_name = ?),
                    app_name = ?,
                    login = ?,
                    password = ?
                    WHERE id = ?
                    """, validator(args) + validator(id))
        self.con.commit()
        self.clean_unused_categories(old_category)

    def get_id(self, args):
        cur = self.con.cursor()
        return cur.execute("""
                           SELECT id
                           FROM Passwords
                           WHERE  app_type =
                           (SELECT id FROM Types
                           WHERE type_name = ?)
                           AND app_name = ?
                           AND login = ?
                           """, validator(args[:3])).fetchone()

    def delete(self, id):
        cur = self.con.cursor()
        old_category = self.get_category(id)
        cur.execute("""
                    DELETE FROM Passwords
                    WHERE id = ?
                    """, validator(id))
        self.con.commit()
        self.clean_unused_categories(old_category)

    def del_category(self, category):
        cur = self.con.cursor()
        cur.execute("""
                    DELETE FROM Types
                    WHERE type_name = ?
                    """, validator(category))
        self.con.commit()

    def clean_unused_categories(self, category):
        if not self.is_category(category):
            self.del_category(category)
