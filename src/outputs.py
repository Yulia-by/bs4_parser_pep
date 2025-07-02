import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import (
    BASE_DIR,
    DATETIME_FORMAT,
    RESULTS_DIR_NAME,
    FILE_ARGUMENT_NAME,
    PRETTY_ARGUMENT_NAME
)


def control_output(results, cli_args):
    output_function = OUTPUT_FUNCTIONS.get(cli_args.output,
                                           OUTPUT_FUNCTIONS[None])
    if cli_args.output == FILE_ARGUMENT_NAME:
        output_function(results, cli_args)
    else:
        output_function(results)


def default_output(results):
    for row in results:
        print(*row)


def pretty_output(results):
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(results, cli_args):
    results_dir = BASE_DIR / RESULTS_DIR_NAME
    results_dir.mkdir(exist_ok=True)
    mode = cli_args.mode
    timestamp = dt.datetime.now().strftime(DATETIME_FORMAT)
    filename = f"{mode}_{timestamp}.csv"
    filepath = results_dir / filename
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, dialect='unix')
        writer.writerows(results)
    logging.info(f'Файл с результатами успешно сохранён: {filepath}')


OUTPUT_FUNCTIONS = {
    PRETTY_ARGUMENT_NAME: pretty_output,
    FILE_ARGUMENT_NAME: file_output,
    None: default_output,
}
