import csv
from datetime import datetime

from tabulate import tabulate

data_dir = '../data'
time_format = '%Y-%m-%d %H:%M'
min_c = 10
max_c = 50

RESET = "\033[0m"
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

# Bright colors
BRIGHT_BLACK = "\033[90m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"
BRIGHT_WHITE = "\033[97m"

# Background colors
BG_BLACK = "\033[40m"
BG_GRAY = "\033[100m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
BG_WHITE = "\033[47m"

# Bright background colors
BG_BRIGHT_BLACK = "\033[100m"
BG_BRIGHT_RED = "\033[101m"
BG_BRIGHT_GREEN = "\033[102m"
BG_BRIGHT_YELLOW = "\033[103m"
BG_BRIGHT_BLUE = "\033[104m"
BG_BRIGHT_MAGENTA = "\033[105m"
BG_BRIGHT_CYAN = "\033[106m"
BG_BRIGHT_WHITE = "\033[107m"

def get_data(file_name) -> dict:
    data = {}

    with open(f'{data_dir}/{file_name}.csv', 'r') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            date_object = datetime.strptime(row['TIME'], time_format)

            key = f'{date_object.year}-{date_object.month:02d}-{date_object.day:02d}'

            if key not in data:
                data[key] = {}

            if date_object.hour not in data[key]:
                data[key][date_object.hour] = 0

            data[key][date_object.hour] += 1

    return dict(sorted(data.items()))

def get_colour(count: int) -> str:
    colour = BG_GRAY + BLACK

    if 0 <= count <= min_c:
        colour = BG_BLACK + WHITE
    elif max_c < count <= 60:
        colour = BG_WHITE + BLACK

    return colour

def get_table(data: dict) -> list[list[str]]:
    headers = [f'{i:02d}' for i in range(24)]
    headers.insert(0, 'День')
    table = [headers]

    for day_name, day_data in data.items():
        day = [day_name]
        for i in range(24):
            count = day_data.get(i, 0)
            day.append(f'{get_colour(count)}{count:^4d}{RESET}')

        table.append(day)

    return table

if __name__ == '__main__':
    file_name = '20240701_12'
    data = get_data(file_name)
    table = get_table(data)
    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
