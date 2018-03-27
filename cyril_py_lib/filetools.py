from os import listdir
import os.path
import time


def file_list(path, contains=None, suffix=None, contains_any=None, suffix_any=None, contains_all=None,
              return_full_path=False):
    """
    Potentially filtered file names from path
    :param path: String absolute or relative (from execution place) path
    :param contains: String contained in filename
    :param suffix: String file type (after last dot)
    :param contains_all:  List of strings (analogue to contains parameter) Can't use in combination other 'contains'
    :param contains_any: List of strings (analogue to contains parameter) Can't use in combination with 'contains'
    :param suffix_any: List of strings (analogue to suffix parameter) Can't use in combination with 'suffix'
    :param return_full_path: If set to True, returns list of valid paths, else only file names.
    :return: List of only the file names (not paths)
    """
    if contains and contains_any or contains and contains_all or contains_any and contains_all:
        raise AttributeError('Specify only one of "contains", "contains_any" or "contains_all" parameters.')
    if suffix and suffix_any:
        raise AttributeError('Specify either "suffix" or "suffix_any" parameter, not both.')

    files = listdir(path)
    if contains:
        files = [f for f in files if contains in f]
    if suffix:
        len_suffix = len(suffix)
        files = [f for f in files if f[-1*len_suffix:] == suffix]

    if contains_all:
        for c in contains_all:
            files = [f for f in files if c in f]
    if contains_any:
        files_to_return = []
        for c in contains_any:
            files_to_return += [f for f in files if c in f]
        files = files_to_return
    if suffix_any:
        files_to_return = []
        for s in suffix_any:
            len_suffix = len(s)
            files_to_return += [f for f in files if f[-1*len_suffix:] == s]
        files = files_to_return
    if return_full_path:
        return [os.path.join(path, f) for f in files]
    else:
        return files


def file_info(path, single_string=True):
    """
    Function to provide file info as string for e.g. logging.
    :param path: A valid path to a file.
    :param single_string: Default True means returns single string for e.g. logging. False returns 3 separate strings,
           with file size in bytes.
    :return: String(s) containing modification date, creation date and file size in KB.
    """
    mod_date = time.ctime(os.path.getmtime(path))
    cre_date = time.ctime(os.path.getctime(path))
    size = os.path.getsize(path)/1024.0
    if single_string:
        return "Last modified: {}\t Created: {}\t Size: {} KB".format(mod_date, cre_date, size)
    else:
        return mod_date, cre_date, size*1024
