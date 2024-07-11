import csv
from datetime import datetime

from tabulate import tabulate

data_dir = '../data'
time_format = '%Y-%m-%d %H:%M'

BG_BLACK = "\033[40m"
BG_GRAY = "\033[100m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
BG_WHITE = "\033[47m"

RESET = "\033[0m"

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
    colour = BG_GRAY

    if 0 <= count <= 15:
        colour = BG_BLACK
    elif 45 < count <= 60:
        colour = BG_WHITE

    return colour

def get_table(data: dict) -> list[list[str]]:
    headers = [f'{i+1:02d}' for i in range(24)]
    headers.insert(0, 'День')
    table = [headers]

    for day_name, day_data in data.items():
        day = [day_name]
        for i in range(24):
            count = day_data.get(i, 0)
            day.append(f'{get_colour(count)}{count}{RESET}')

        table.append(day)

    return table

if __name__ == '__main__':
    file_name = '20240709_11'
    data = get_data(file_name)
    table = get_table(data)
    print(tabulate(table, headers='firstrow'))
