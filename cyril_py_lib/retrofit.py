def correct_missing(rel_week):
    if rel_week <= 38:
        return rel_week - 1
    else:
        return rel_week


def standard_wy(week=None, year=None):
    if not (week and year):
        raise AttributeError("Both 'week' and 'year' have to be defined.")
    if not isinstance(year, int):
        year = int(year)
    if year <= 99:
        year += 2000
    assert 2015 < year < 2020, "Year is in wrong range: {}".format(year)
    if not isinstance(week, int):
        week = int(week)
    # make strings out of them
    week_str = str(week)
    year_str = str(year)
    if len(week_str) == 1:
        week_str = "0" + week_str
    return int(year_str + week_str)


class SafeDate:

    def __init__(self, week, year):
        self.week = self.check_allowed_week(int(week))
        self.year = self.check_allowed_year(int(year))
        self.year_week_string = standard_wy(week, year)
        self.rel_week = correct_missing(self.make_relative())

    @staticmethod
    def check_allowed_week(week_int):
        if not 1 <= week_int <= 52:
            raise ValueError("Week has to be between 1 and 52. Got {}".format(week_int))
        return week_int

    @staticmethod
    def check_allowed_year(year_int):
        if not 2016 <= year_int <= 2019:
            if not 15 <= year_int <= 19:
                raise ValueError("Year has to be between 16 and 19 or 2016 and 2019. Got {}".format(year_int))
            else:
                year_int += 2000
                if not 2016 <= year_int <= 2019:
                    raise ValueError("Year has to be between 16 and 19 or 2016 and 2019. Got {}".format(year_int - 2000))
        return year_int

    def make_relative(self):
        if self.year == 2017:
            return self.week
        else:
            del_yrs = self.year - 2017
            return del_yrs*52 + self.week

    def __str__(self):
        return str(self.week)+"_"+str(self.year)

    def __eq__(self, other):
        return self.rel_week == other.rel_week

    def __gt__(self, other):
        return self.rel_week > other.rel_week

    def __lt__(self, other):
        return self.rel_week < other.rel_week

    def __le__(self, other):
        return self.rel_week <= other.rel_week

    def __ge__(self, other):
        return self.rel_week >= other.rel_week

    def __ne__(self, other):
        return self.rel_week != other.rel_week

    def __sub__(self, other):
        return self.rel_week - other.rel_week
