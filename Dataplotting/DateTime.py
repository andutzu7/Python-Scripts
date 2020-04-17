from dateutil.parser import parse


class DateFunctions:
    @staticmethod
    def get_separator(string):
        for char in string:
            if not char.isnumeric():
                return char

    @staticmethod
    def is_date(string, fuzzy=False):
        try:
            parse(string)
            print(type(string))
            return True

        except ValueError:
            return False

    @staticmethod
    def extract_year(tokens):
        year = 0
        for x in tokens:
            if x.isdigit():
                val = int(x)
                if val > 0:
                    if val > year:
                        year = val
        return year
