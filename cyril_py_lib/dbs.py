import sqlite3 as sql
from sqlite3 import OperationalError
from sqlite3 import IntegrityError
import os


class PathError(Exception):
    pass


class Database:

    def __init__(self, path):
        """
        Initialisation of a db handler. The db handler allows to perform the essential db operations.
        :param path: A valid path (possibly non-existing) to the (to be created or existing) db.
        """
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

    def open(self):
        """
        Function to reopen a closed db.
        :return: Nothing is returned.
        """
        self.con = sql.connect(self.db_path)
        self.c = self.con.cursor()
        self.guess_working_table()

    def table(self):
        """
        Function to get the name of the current working table.
        :return: String, name of current working table.
        """
        return self.working_table

    def set_table(self, new_table):
        """
        Function to change the current working table to new_table. Checks if new_table exists in tables, else throws
        error.
        :param new_table: String, name of new table.
        :return: void
        """
        if new_table in self.tables():
            self.working_table = new_table
        else:
            raise KeyError("Suggested table '{}' not in existing tables: {}".format(new_table, str(self.tables())))

    def guess_working_table(self):
        """
        Tries to find tables already existing in the db and set 'working_table' attribute accordingly. If no table
        is found, it is set to 'None' if multiple tables are found, 'working_table' is set "randomly".
        :return: Nothing is returned.
        """
        try:
            table_names = self.tables()
            self.working_table = table_names[0]
        except (OperationalError, IndexError):
            self.working_table = None

    def create_table(self, table_name, list_of_col_names, list_of_col_types, unique_combination=None):
        """
        Creates a new table in the db of the instance if it doesn't already exist. Sets the 'working_table' attribute
        of the class instance to the newly created table (also if table already existed). If a single column shall be
        of constraint unique, it can be declared in the column type definition. E.g. "text unique".
        :param table_name: String of the table name, which is to be created.
        :param list_of_col_names: List of strings containing the column names to be created.
        :param list_of_col_types: List of strings. List of same length as list_of_col_names, holding the types of
        the column at the matching index. Supported types are: 'text', 'integer', 'real', 'blob' (anything at all). For
        example the 'real' type can also hold a python string. But only if 'real' is specified (instead of 'text' or
        'blob', the numerical conditions will be correct (e.g. >= 5).
        :param unique_combination: Optional list of names (which are already present in 'list_of_col_names'). When
        inserting new elements into the table, the combination of these column's values have to be unique.
        :return: Nothing is returned.
        """
        self.working_table = table_name
        create_table_string = self.creation_string(list_of_col_names, list_of_col_types, unique_combination)
        try:
            self.c.execute(create_table_string)
        except OperationalError as e:
            print(create_table_string)
            raise e
        self.commit()

    @staticmethod
    def guess_col_types(list_of_col_types):
        """
        Function to autodetect (guess) types of columns - for table creation - using an example row. Return elements
        can be TEXT and REAL.
        :param list_of_col_types: List of an example row. Has to have same length as list_of_col_names.
        :return: List of db types guess. Can be used in 'create_table'
        """
        types = []
        for e in list_of_col_types:
            if isinstance(e, (int, float)):
                types.append("real")
            else:
                types.append("text")
        return types

    def check_if_table_exists(self, name):
        """
        Function to check if a particular table already exists in the db of the class instance. The 'working_table'
        class attribute is not changed by this function.
        :param name: String of the table name for which to check.
        :return: True or False, depending weather the table already exists.
        """
        return name in self.tables()

    def commit(self):
        """
        Function to commit all staged db operations.
        :return: Nothing is returned.
        """
        self.con.commit()

    def close(self):
        """
        Function to close the connection to the db of the instance. Can later be reopened with 'classInstance.open()'.
        :return: Nothing is returned.
        """
        self.con.close()

    def recreate_table(self, table_to_recreate):
        # todo: continue
        pass

    def tables(self):
        """
        Function to find out which tables are held by the db.
        :return: List of strings of the table names.
        """
        res = self.con.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [n[0] for n in res]

    def tables_with_columns(self):
        """
        Informative function to find out which tables are held by the db and what the column names of the tables are.
        :return: List of list of strings or single empty list.
        """
        current_table = self.working_table
        tables = self.tables()
        result = []
        for t in tables:
            self.working_table = t
            result.append([t, str(self.column_names())])
        self.working_table = current_table
        return result

    def delete_table(self, table_to_drop):
        self.c.execute("drop table if exists {}".format(table_to_drop))

    def drop_table(self, table_to_drop=None):
        if not table_to_drop:
            table_to_drop = self.working_table
        self.delete_table(table_to_drop)
        self.guess_working_table()
        return "Working table changed to {}".format(self.working_table)

    def column_names(self):
        cursor = self.con.execute("select * from {}".format(self.working_table))
        return [d[0] for d in cursor.description]

    def column_types(self):
        cursor = self.con.execute("select * from {}".format(self.working_table))
        return [d for d in cursor.description]

    def creation_string(self, col_names, col_types, unique_combination):
        nr_names = len(col_names)
        nr_types = len(col_types)
        assert_msg = "Name and type list don't have same length: "
        assert nr_names == nr_types, assert_msg + "{} names and {} types provided".format(nr_names, nr_types)
        prefix = "CREATE TABLE IF NOT EXISTS {} ".format(self.working_table)
        bracket = "("
        for n, t in zip(col_names, col_types):
            bracket += "{} {},".format(n, t)
        bracket = bracket[:-1] + ")"
        if unique_combination:
            err_msg = "only tuple of unique constraint implemented so far. Provided {}".format(len(unique_combination))
            assert len(unique_combination) == 2, err_msg
            u1, u2 = unique_combination[0], unique_combination[1]
            append = ", constraint unique_combination unique ({}, {})".format(u1, u2)
            bracket = bracket[:-1] + append + ")"
        return prefix + bracket

    def write_entry(self, *args):
        if len(args) == 1:
            string = "insert into {} values ({})".format(self.working_table, self.string_with_spaces(*args)[1:-1])
        else:
            string = "insert into {} values {}".format(self.working_table, self.string_with_spaces(args))
        self.execute(string)

    def execute(self, string):
        try:
            self.c.execute(string)
        except OperationalError as e:
            print(string)
            raise e
        except IntegrityError as e:
            if e.__str__()[:6] == "UNIQUE":
                pass
            else:
                raise e

    def query_column(self, col_name):
        """
        Function to query all elements from one column.
        :param col_name: Name of the column to query.
        :return: List of all elements of the queried column.
        """
        string = "select {} from {}".format(col_name, self.working_table)
        self.execute(string)
        return [r[0] for r in self.c.fetchall()]

    def query_column_uniques(self, col_name):
        """
        Function to get the unique entries of a column. Utilises query_column.
        :param col_name: String, name of the column to query.
        :return: List of unique elements of the queried column.
        """
        return list(set(self.query_column(col_name)))

    def query_where(self, *columns_and_values):
        """
        Function to collect whole db elements where criteria are met.
        :param columns_and_values: Unspecified number of string pairs: "col_name>", "value"
        :return: List of list of whole db elements that match criteria.
        """
        string = "select * from {} where {}".format(self.working_table, self.string_with_dic_and(*columns_and_values))
        try:
            self.c.execute(string)
        except OperationalError as e:
            print(string)
            raise e
        return [list(i) for i in self.c.fetchall()]

    def query_string(self, query_string):
        self.c.execute(query_string)
        return [list(i) for i in self.c.fetchall()]

    @staticmethod
    def string_with_dic_and(*columns_values):
        cols = []
        values = []
        for i, v in enumerate(columns_values):
            if i % 2 == 0:
                cols.append(v)
            else:
                values.append(v)
        string = ""
        e_msg = "wrong number of arguments: {} columns and {} values provided".format(len(cols), len(values))
        assert len(cols) == len(values), e_msg
        for c, v in zip(cols, values):
            string += "{}'{}' and ".format(c, v)
        return string[:-5]

    @staticmethod
    def string_with_spaces(*args):
        r = ""
        for a in args:
            r += str(a)+" "
        return r[:-1]

    def write_entries(self, list_of_lists):
        """
        Function to write multiple entries at once. Utilises self.write_entry to write.
        :param list_of_lists: A list containing lists of elements to be inserted into db table.
        :return: void
        """
        for li in list_of_lists:
            self.write_entry(li)


