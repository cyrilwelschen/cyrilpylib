import os


def file_list(path, contains=None, suffix=None, contains_any=None, suffix_any=None, contains_all=None):
    """
    Potentially filtered file names from path
    :param path: String absolute or relative (from execution place) path
    :param contains: String contained in filename
    :param suffix: String file type (after last dot)
    :param contains_all:  List of strings (analogue to contains parameter) Can't use in combination other 'contains'
    :param contains_any: List of strings (analogue to contains parameter) Can't use in combination with 'contains'
    :param suffix_any: List of strings (analogue to suffix parameter) Can't use in combination with 'suffix'
    :return: List of only the file names (not paths)
    """
    if contains and contains_any or contains and contains_all or contains_any and contains_all:
        raise AttributeError('Specify only one of "contains", "contains_any" or "contains_all" parameters.')
    if suffix and suffix_any:
        raise AttributeError('Specify either "suffix" or "suffix_any" parameter, not both.')

    files = os.listdir(path)
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
    return files
