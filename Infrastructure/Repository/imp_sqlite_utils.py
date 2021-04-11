import sqlite3


def connection_to_db(func):
    database_name = 'Database.db'

    def wrap_func(*args, **kwargs):
        connection = None
        try:
            connection = sqlite3.connect(database_name)
            cursor = connection.cursor()
            result = func(cursor=cursor, *args, **kwargs)
            return result
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if connection:
                connection.close()
                #print("The SQLite connection is closed")
    return wrap_func
