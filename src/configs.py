import argparse
import logging

from constants import (
    BASE_DIR,
    PRETTY_ARGUMENT_NAME,
    FILE_ARGUMENT_NAME,
    LOG_DIR_NAME,
    LOG_FILE_NAME
)

from logging.handlers import RotatingFileHandler


LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'


def configure_argument_parser(available_modes):
    parser = argparse.ArgumentParser(description='Парсер документации Python')
    parser.add_argument(
        'mode',
        choices=available_modes,
        help='Режимы работы парсера'
    )
    parser.add_argument(
        '-c',
        '--clear-cache',
        action='store_true',
        help='Очистка кеша'
    )
    parser.add_argument(
        '-o',
        '--output',
        choices=(PRETTY_ARGUMENT_NAME, FILE_ARGUMENT_NAME),
        help='Дополнительные способы вывода данных'
    )
    return parser


def configure_logging():
    log_dir = BASE_DIR / LOG_DIR_NAME
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / LOG_FILE_NAME
    rotating_handler = RotatingFileHandler(
        log_file, maxBytes=10 ** 6, backupCount=5
    )
    logging.basicConfig(
        datefmt=DT_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler())
    )
