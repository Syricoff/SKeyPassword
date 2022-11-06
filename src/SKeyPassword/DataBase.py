import sqlite3


class DataBase:
    def __init__(self):
        self.con = sqlite3.connect("res/passwords.sqlite")

    def validator(self, args):
        return tuple(map(lambda x: x.lower().title(), args))

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
                    WHERE id IN
                    (SELECT app_type FROM Passwords)
                    ''').fetchall()))

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
                           """, (id,)
                           ).fetchone()

    def loadId(self, filter='', condition='', args=tuple()) -> tuple[int]:
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
                         ''', self.validator((condition,))).fetchall()))
        elif filter == "Приложения" and condition:
            return tuple(map(lambda x: int(x[0]),
                         cur.execute('''
                         SELECT id
                         FROM Passwords
                         WHERE app_name = ?
                         ''', self.validator((condition,))).fetchall()))
        elif filter == "id" and args:
            return cur.execute("""
                            SELECT id
                            FROM Passwords
                            WHERE  app_type =
                            (SELECT id FROM Types
                            WHERE type_name = ?)
                            AND app_name = ?
                            AND login = ?
                            """, self.validator(args[:3])).fetchall()
        return tuple(map(lambda x: int(x[0]),
                         cur.execute('''
                         SELECT id
                         FROM Passwords
                         ''').fetchall()))

    def add(self, args):
        cur = self.con.cursor()
        self.addCategoryIf(args)
        cur.execute("""
                    INSERT INTO
                    Passwords(app_type, app_name, login, password)
                    VALUES((SELECT id FROM Types WHERE
                    type_name = ?), ?, ?, ?)
                    """, self.validator(args))
        self.con.commit()

    def addCategoryIf(self, category):
        """Проверяет есть ли категория в базе данных
                        и если нет, добавляет её туда"""
        cur = self.con.cursor()
        result = cur.execute('''
                             SELECT * FROM types
                             WHERE type_name = ?
                             ''', self.validator(category[:1]))
        if not result.fetchone():
            cur.execute('''
                        INSERT INTO Types(type_name)
                        VALUES(?)
                        ''', self.validator(category[:1]))
            self.con.commit()

    def overwrite(self, id, args):
        cur = self.con.cursor()
        self.addCategoryIf(args)
        cur.execute("""
                    UPDATE Passwords
                    SET app_type =
                    (SELECT id FROM Types
                    WHERE type_name = ?),
                    app_name = ?,
                    login = ?,
                    password = ?
                    WHERE id = ?
                    """, self.validator(args) + (id,))
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
                    """, (id,))
        self.con.commit()
