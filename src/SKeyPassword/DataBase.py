import sqlite3


def validator(args):
    # Приводит данные к удобному для запросов виду
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
        # Подключаем базу данных
        self.con = sqlite3.connect("passwords.sqlite")

    def __new__(cls):
        """Синглтон"""
        if not hasattr(cls, 'instance'):
            cls.instance = super(DataBase, cls).__new__(cls)
        return cls.instance

    def change_db(self, path):
        """Подключает пользовательску базу данных"""
        self.con = sqlite3.connect(path)

    def is_category(self, category):
        """Проверяет используется ли категория"""
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
        """Возвращает кортеж (категория, приложение, логин, пароль) по id"""
        cur = self.con.cursor()
        return cur.execute("""
                           SELECT
                           (SELECT type_name
                           FROM Types
                           WHERE app_type = id),
                           app_name,
                           login, password
                           FROM Passwords
                           WHERE id = ?
                           """, validator(id)
                           ).fetchone()

    def get_category(self, id):
        return self.get_entry(id)[0]

    def get_apps(self, conditin=None) -> tuple[str] | None:
        """Возвращает кортеж приложений"""
        cur = self.con.cursor()
        if conditin:
            return tuple(map(lambda x: x[0],
                             cur.execute('''
                                         SELECT DISTINCT app_name
                                         FROM Passwords
                                         WHERE app_type = (
                                         SELECT id
                                         FROM Types
                                         WHERE type_name = ?)
                                         ''', validator(conditin)
                                         ).fetchall()))
        return tuple(map(lambda x: x[0],
                         cur.execute('''
                                    SELECT DISTINCT app_name
                                    FROM Passwords '''
                                     ).fetchall()))

    def get_categories(self) -> tuple[str]:
        """Возвращает кортеж категорий"""
        cur = self.con.cursor()
        return tuple(map(lambda x: x[0],
                         cur.execute('''
                                    SELECT type_name
                                    FROM Types
                                    ''').fetchall()))

    def load_id(self, app=None, category=None) -> tuple[int] | None:
        """Загружает и возвращает кортеж id записей"""
        cur = self.con.cursor()
        if app and category:
            return tuple(map(lambda x: int(x[0]),
                             cur.execute('''
                                         SELECT id
                                         FROM Passwords
                                         WHERE app_name = ?
                                         AND app_type = (
                                         SELECT id
                                         FROM Types
                                         WHERE type_name = ?)
                                         ''', validator((app, category))
                                         ).fetchall()))
        elif app:
            return tuple(map(lambda x: int(x[0]),
                             cur.execute('''
                                         SELECT id
                                         FROM Passwords
                                         WHERE app_name = ?
                                         ''', validator(app)
                                         ).fetchall()))
        elif category:
            return tuple(map(lambda x: int(x[0]),
                             cur.execute('''
                                         SELECT id
                                         FROM Passwords
                                         WHERE app_type =
                                         (SELECT id
                                         FROM Types
                                         WHERE type_name = ?)
                                         ''', validator(category)
                                         ).fetchall()))
        return tuple(map(lambda x: int(x[0]),
                         cur.execute('''
                                     SELECT id
                                     FROM Passwords
                                     ''').fetchall()))

    def add(self, args):
        """Добавляет новую запись в базу данных """
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
        """Перезаписывает запись в базе данных"""
        cur = self.con.cursor()
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
        self.clean_unused_categories()

    def get_id(self, args):
        """Возвращает id записи по её данным или None"""
        cur = self.con.cursor()
        res = cur.execute("""
                          SELECT id
                          FROM Passwords
                          WHERE app_name = ?
                          AND login = ?
                          """, validator(args[1:3])).fetchone()
        return res[0] if type(res) == tuple else res

    def delete(self, id):
        """Удаляет запись из базы данных"""
        cur = self.con.cursor()
        cur.execute("""
                    DELETE FROM Passwords
                    WHERE id = ?
                    """, validator(id))
        self.con.commit()
        self.clean_unused_categories()

    def clean_unused_categories(self):
        """Очищает базу данных от неиспользуемых категорий"""
        cur = self.con.cursor()
        cur.execute("""
                    DELETE FROM Types
                    WHERE id NOT IN (
                    SELECT app_type
                    FROM Passwords)
                    """)
        self.con.commit()
