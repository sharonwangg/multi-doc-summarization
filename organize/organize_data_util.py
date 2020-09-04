def get_months():
    return [[1, 'january'],
              [1, 'jan'],
              [2, 'february'],
              [2, 'feb'],
              [3, 'march'],
              [3, 'mar'],
              [4, 'april'],
              [4, 'apr'],
              [5, 'may'],
              [6, 'june'],
              [6, 'jun'],
              [7, 'july'],
              [7, 'jul'],
              [8, 'august'],
              [8, 'aug'],
              [9, 'september'],
              [9, 'sept'],
              [10, 'october'],
              [10, 'oct'],
              [11, 'november'],
              [11, 'nov'],
              [12, 'december'],
              [12, 'dec']]


def get_weekdays():
    return [[1, 'monday'],
                [1, 'mon'],
                [2, 'tuesday'],
                [2, 'tues'],
                [3, 'wednesday'],
                [3, 'wed'],
                [4, 'thursday'],
                [4, 'thurs'],
                [5, 'friday'],
                [5, 'fri'],
                [6, 'saturday'],
                [6, 'sat'],
                [7, 'sunday'],
                [7, 'sun']]


def get_ordinal_indicators():
    return ['st', 'nd', 'rd', 'th']


MONTHS = get_months()
WEEKDAYS = get_weekdays()
ORDINAL_INDICATORS = get_ordinal_indicators()