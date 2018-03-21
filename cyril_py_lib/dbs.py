import sqlite3 as sql
from sqlite3 import OperationalError
import os


class PathError(Exception):
    pass


class Database:

    def __init__(self, path):
        assert path[-len(".db"):] == ".db", "Provided path doesn't lead to a .db file"
        try:
            if not os.path.exists(path):
                with open(path, 'w'):
                    pass
        except FileNotFoundError:
            raise PathError("Provided path {} is invalid.".format(path))
        self.db_path = path
        self.con = sql.connect(self.db_path)
        self.c = self.con.cursor()
        self.working_table = None
        self.guess_working_table()

    def guess_working_table(self):
        try:
            table_names = self.tables()
            self.working_table = table_names[0]
        except OperationalError:
            self.working_table = None

    def create_table(self, table_name, list_of_col_names, list_of_col_types):
        # todo: can be made much smaller b/c now we are in class!
        self.working_table = table_name
        supported_types = ["text", "integer", "real"]
        for t in list_of_col_types:
            if t not in supported_types:
                raise TypeError("{} not in list of supported database types: {}".format(t, supported_types))
        connection = sql.connect(self.db_path)
        cursor = connection.cursor()
        # todo: option to recreate
        # todo: handle existing table
        # cursor.execute("DROP TABLE IF EXISTS {}".format(table_name))
        create_table_string = self.creation_string(list_of_col_names, list_of_col_types)
        cursor.execute(create_table_string)
        connection.commit()
        connection.close()

    def check_if_table_exists(self):
        pass

    def exe(self):
        pass

    def commit(self):
        self.con.commit()

    def close_db(self):
        self.con.close()

    def recreate_table(self):
        # self.c.execute("")
        pass

    def create_versioned_table(self):
        pass

    def tables(self):
        res = self.con.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [n[0] for n in res]

    def tables_with_columns(self):
        current_table = self.working_table
        tables = self.tables()
        result = []
        for t in tables:
            self.working_table = t
            result.append([t, self.column_names()])
        self.working_table = current_table
        return result

    def drop_table(self, table_to_drop=None):
        if not table_to_drop:
            table_to_drop = self.working_table
        self.c.execute("drop table if exists {}".format(table_to_drop))
        self.guess_working_table()
        return "Working table changed to {}".format(self.working_table)

    def column_names(self):
        cursor = self.con.execute("select * from {}".format(self.working_table))
        return [d[0] for d in cursor.description]

    def creation_string(self, col_names, col_types):
        nr_names = len(col_names)
        nr_types = len(col_types)
        assert_msg = "Name and type list don't have same length: "
        assert nr_names == nr_types, assert_msg + "{} names and {} types provided".format(nr_names, nr_types)
        # todo: alternative when already exists
        prefix = "CREATE TABLE IF NOT EXISTS {} ".format(self.working_table)
        bracket = "("
        for n, t in zip(col_names, col_types):
            bracket += "{} {},".format(n, t)
        bracket = bracket[:-1] + ")"
        return prefix + bracket

    def write_single_entry(self):
        pass

    def write_multiple_entries(self):
        pass
