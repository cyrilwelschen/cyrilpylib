import datetime
from pandas import DataFrame


def xldate_to_datetime(excel_date):
    """
    Function to convert excel date "432..." to normal date
    :param excel_date:
    :return:
    """
    temp_starting_point = datetime.datetime(1899, 12, 30)
    delta = datetime.timedelta(days=excel_date)
    return temp_starting_point + delta


def write_to_excel(filename, lists, sheet_name="sheet_1", index=False):
    df = DataFrame(lists)
    df.to_excel(filename, sheet_name=sheet_name, index=index)
