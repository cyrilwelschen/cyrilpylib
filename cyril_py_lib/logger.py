import os.path
from time import strftime


class Logger:

    def __init__(self, path_to_files):
        self.log_file = os.path.join(path_to_files, "log.txt")
        self.err_file = os.path.join(path_to_files, "err.txt")
        self.create_files()

    def create_files(self):
        date = strftime("%d.%m.%Y")
        time = strftime("%H:%M")
        log_msg = "### This is a log file created on the {} at {}. ###".format(date, time)
        err_msg = "### This is an error file created on the {} at {}. ###".format(date, time)
        self.write(self.log_file, log_msg)
        self.write(self.err_file, err_msg)

    @staticmethod
    def write(file_path, string):
        if not string[-2:] == "\n":
            string += "\n"
        with open(file_path, 'a') as f:
            f.write(string)
        f.close()

    def log(self, string):
        self.write(self.log_file, string)

    def err(self, string):
        self.write(self.err_file, string)
