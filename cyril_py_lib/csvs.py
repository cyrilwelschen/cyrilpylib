import csv
import xlrd


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


def read_csv(file_path, axis="row", delimiter=";", starting_point=0, ending_point=None):
    """
    Read a csv data file.
    :param file_path: string: relative or abs path to csv file.
    :param axis: return arranged along rows (default) or columns ("col").
    :param delimiter: string with which delimiter csv file is encoded. Default ";".
    :param starting_point: integer: index where to start return
           (e.g. 2  with "axis='row'"-> gives back from third row on)
    :param ending_point: integer: same as starting_point but from the end
    :return: List of lists of content of csv file.
    """
    with open(file_path, 'r') as f:
        reader = csv.reader(f, delimiter=delimiter)
        data = list(reader)
    if axis == "col":
        data = list(map(list, zip(*data)))
    if not ending_point:
        ending_point = len(data)
    else:
        if ending_point > len(data):
            ending_point = len(data)
    return data[starting_point:ending_point]


def csv_from_excel(path_to_excel):
    wb = xlrd.open_workbook(path_to_excel)
    shs = wb.sheet_names()
    sh = wb.sheet_by_name(shs[0])
    suffix_length = 3
    if path_to_excel[-4:] == "xlsx":
        suffix_length = 4
    new_csv = open(path_to_excel[:-suffix_length]+"csv", 'w', newline='')
    wr = csv.writer(new_csv)
    for row_num in range(sh.nrows):
        wr.writerow(sh.row_values(row_num))
    new_csv.close()
