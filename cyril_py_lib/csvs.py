import csv


def peek_csv(file_path, axis="row", nr_of_rows=10, delimiter=";"):
    """
    Take a peek at a csv without reading the entire file into buffer.
    :param file_path: string abs or rel path to file
    :param axis: return arranged along rows (default) or columns ("col")
    :param nr_of_rows: integer indicating numbers of rows to read (all columns are read)
    :param delimiter: string with which delimiter csv file is encoded. Default ";"
    :return: List of lists of content of beginning of csv file.
    """
    peek = []
    with open(file_path, 'r') as f:
        reader = csv.reader(f, delimiter=delimiter)
        counter = 0
        while counter < nr_of_rows:
            try:
                peek.append(list(next(reader)))
            except StopIteration:
                counter = nr_of_rows
            counter += 1
    if axis == "col":
        peek = list(map(list, zip(*peek)))
    return peek


def read_csv(file_path, axis="row", delimiter=";"):
    """
    Read a csv data file.
    :param file_path: string: relative or abs path to csv file.
    :param axis: return arranged along rows (default) or columns ("col").
    :param delimiter: string with which delimiter csv file is encoded. Default ";".
    :return: List of lists of content of csv file.
    """
    with open(file_path, 'r') as f:
        reader = csv.reader(f, delimiter=delimiter)
        data = list(reader)
    if axis == "col":
        data = list(map(list, zip(*data)))
    return data
