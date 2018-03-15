import sqlite3 as sql


class Database:

    def __init__(self, path):
        self.db_path = path
        self.working_table = None

    def create_table(self, table_name, list_of_col_names, list_of_col_types):
        supported_types = ["text", "integer", "real"]
        for t in list_of_col_types:
            if t not in supported_types:
                raise TypeError("{} not in list of supported database types: {}".format(t, supported_types))
        connection = sql.connect(self.db_path)
        cursor = connection.cursor()
        # todo: option to recreate
        # todo: handle existing table
        # cursor.execute("DROP TABLE IF EXISTS {}".format(table_name))
        create_table_string = creation_string(table_name, list_of_col_names, list_of_col_types)
        cursor.execute(create_table_string)
        connection.commit()
        connection.close()

    def check_if_table_exists():
        pass

    def exe():
        pass

    def close_connection():
        pass

    def create_connection():
        pass

    def recreate_table():
        pass

    def create_versioned_table():
        pass

    def show_tables():
        pass

    def show_tables_with_colnames():
        pass

    def show_colnames_of_table():
        pass

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

    def write_single_entry():
        pass

    def write_multiple_entries():
        pass
