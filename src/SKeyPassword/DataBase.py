import sqlite3


class DataBase:
    def __init__(self):
        self.con = sqlite3.connect("res/passwords.sqlite")

    def validator(self, args):
        if type(args) is str:
            return (args.lower().title(), )
        elif type(args) is int:
            return (args, )
        elif any(map(lambda x: type(x) == int, args)):
            return args
        return tuple(
                    map(lambda x: x.strip().lower().title(), args[:3])
                    ) + args[3:]

    def isCategory(self, category):
        cur = self.con.cursor()
        return bool(cur.execute('''
                                SELECT id
                                FROM Passwords
                                WHERE app_type =
                                (SELECT id
                                FROM Types
                                WHERE type_name = ?)
                                ''', self.validator(category)).fetchall())

    def getEntry(self, id):
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
                           """, self.validator(id)
                           ).fetchone()

    def getApps(self) -> list[str]:
        """Загружает и возвращает список приложений"""
        cur = self.con.cursor()
        return list(map(lambda x: x[0], cur.execute('''
                    SELECT DISTINCT app_name FROM Passwords
                    ''').fetchall()))

    def getCategories(self) -> list[str]:
        """Загружает и возвращает список категорий"""
        cur = self.con.cursor()
        return list(map(lambda x: x[0], cur.execute('''
                    SELECT type_name
                    FROM Types
                    ''').fetchall()))

    def loadId(self, filter='', condition='') -> tuple[int]:
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
                         ''', self.validator(condition)).fetchall()))
        elif filter == "Приложения" and condition:
            return tuple(map(lambda x: int(x[0]),
                         cur.execute('''
                         SELECT id
                         FROM Passwords
                         WHERE app_name = ?
                         ''', self.validator(condition)).fetchall()))
        return tuple(map(lambda x: int(x[0]),
                         cur.execute('''
                         SELECT id
                         FROM Passwords
                         ''').fetchall()))

    def add(self, args):
        cur = self.con.cursor()
        self.addCategory(args[0])
        cur.execute("""
                    INSERT INTO
                    Passwords(app_type, app_name, login, password)
                    VALUES((SELECT id FROM Types WHERE
                    type_name = ?), ?, ?, ?)
                    """, self.validator(args))
        self.con.commit()

    def addCategory(self, category):
        """Проверяет есть ли категория в базе данных
                        и если нет, добавляет её туда"""
        cur = self.con.cursor()
        if not self.isCategory(category):
            print("d")
            cur.execute('''
                        INSERT INTO Types(type_name)
                        VALUES(?)
                        ''', self.validator(category))
            self.con.commit()

    def overwrite(self, id, args):
        cur = self.con.cursor()
        self.addCategory(args[0])
        cur.execute("""
                    UPDATE Passwords
                    SET app_type =
                    (SELECT id FROM Types
                    WHERE type_name = ?),
                    app_name = ?,
                    login = ?,
                    password = ?
                    WHERE id = ?
                    """, self.validator(args) + self.validator(id))
        self.con.commit()

    def getId(self, args):
        cur = self.con.cursor()
        return cur.execute("""
                            SELECT id
                            FROM Passwords
                            WHERE  app_type =
                            (SELECT id FROM Types
                            WHERE type_name = ?)
                            AND app_name = ?
                            AND login = ?
                            """, self.validator(args[:3])).fetchone()

    def delete(self, id):
        cur = self.con.cursor()
        cur.execute("""
                    DELETE FROM Passwords
                    WHERE id = ?
                    """, self.validator(id))
        self.con.commit()

    def delCategory(self, category):
        cur = self.con.cursor()
        cur.execute("""
                    DELETE FROM Types
                    WHERE type_name = ?
                    """, self.validator(category))
        self.con.commit()
