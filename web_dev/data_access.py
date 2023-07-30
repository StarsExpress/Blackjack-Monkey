import mysql.connector

class DataAccess(object):
    """An object to connect to database."""
    def __init__(self):
        # Connect to database.
        self.mysql_database = mysql.connector.connect(
                host = 'localhost', user = 'root',
                password = 'MadeleineSwann007!', database = 'changshu_aud_test'
        )
        self.mysql_cursor = self.mysql_database.cursor()

    def select(self, sql_syntax, tuple = None):
        if tuple == None:
            self.mysql_cursor.execute(sql_syntax)

        else:
            self.mysql_cursor.execute(sql_syntax, tuple)

    def insert(self, sql_syntax, tuple):
        self.mysql_cursor.execute(sql_syntax, tuple)

    def update(self, sql_syntax, tuple):
        self.mysql_cursor.execute(sql_syntax, tuple)

    def delete(self, sql_syntax, tuple):
        self.mysql_cursor.execute(sql_syntax, tuple)

    def fetchone(self):
        return self.mysql_cursor.fetchone()

    def fetchall(self):
        return self.mysql_cursor.fetchall()

    def commit(self):
        self.mysql_database.commit()

    def save(self):
        self.mysql_database.save()

# Run only if the name is __main__.
if __name__ == '__main__':
    main()