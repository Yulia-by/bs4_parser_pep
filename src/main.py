import logging
import re
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from collections import defaultdict
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (
    BASE_DIR,
    EXPECTED_STATUS,
    MAIN_DOC_URL,
    MAIN_PEP_URL,
    DOWNLOADS_DIR_NAME,
    WHATS_NEW_URL,
    DOWNLOADS_URL
)
from exceptions import NotFoundException
from outputs import control_output
from utils import find_tag, get_soup


def whats_new(session):
    soup = get_soup(session, WHATS_NEW_URL)
    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all('li',
                                              attrs={'class': 'toctree-l1'})
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, автор')]
    for section in tqdm(sections_by_python):
        version_a_tag = find_tag(section, 'a')
        href = version_a_tag['href']
        version_link = urljoin(WHATS_NEW_URL, href)
        soup = get_soup(session, version_link)
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        results.append(
            (version_link, h1.text, dl_text)
        )
    return results


def latest_versions(session):
    soup = get_soup(session, MAIN_DOC_URL)
    sidebar = find_tag(soup, 'div', {'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
        break
    else:
        raise NotFoundException()
    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        link = a_tag['href']
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append(
            (link, version, status)
        )
    return results


def download(session):
    soup = get_soup(session, DOWNLOADS_URL)
    main_tag = find_tag(soup, 'div', {'role': 'main'})
    table_tag = find_tag(main_tag, 'table', {'class': 'docutils'})
    pdf_a4_tag = find_tag(table_tag, 'a',
                          {'href': re.compile(r'.+pdf-a4\.zip$')})
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(DOWNLOADS_URL, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / DOWNLOADS_DIR_NAME
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(f'Архив был загружен и сохранён: {archive_path}')


def pep(session):
    numerical_url = urljoin(MAIN_PEP_URL, 'numerical')
    soup = get_soup(session, numerical_url)
    num_index = find_tag(soup, 'section', {'id': 'numerical-index'})
    tbody = num_index.find('tbody')
    peps_rows = tbody.find_all('tr')
    pep_sum = defaultdict(int)
    for pep_row in peps_rows:
        status_in_page = pep_row.find('abbr').text.strip()[1:]
        url_tag = pep_row.find('a', class_='pep reference internal')
        pep_url = urljoin(MAIN_PEP_URL, url_tag['href'])
        response = session.get(pep_url)
        soup = BeautifulSoup(response.text, features='lxml')
        status_tag = soup.find(
            text='Status').find_parent().next_sibling.next_sibling
        status = status_tag.text.strip()
        try:
            if status not in EXPECTED_STATUS[status_in_page]:
                if len(status_in_page) > 2 or EXPECTED_STATUS[
                        status_in_page] is None:
                    raise KeyError('Получен неожиданный статус')
                logging.info(f'Несовпадающие статусы:\n {pep_url}\n'
                             f'Статус на странице: {status}\n'
                             f'Ожидаемые статусы:\n'
                             f'{EXPECTED_STATUS[status_in_page]}')
        except KeyError as e:
            logging.warning('Получен некорректный статус: %s', str(e))
        else:
            pep_sum[status] += 1
    total_count = sum(pep_sum.values())
    pep_sum['Total'] = total_count
    report = {'Status': 'Count'}
    report.update(dict(sorted(
        (k, v) for k, v in pep_sum.items() if k != 'Total')))
    report['Total'] = pep_sum['Total']
    result = list(report.items())
    return result


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')
    try:
        session = requests_cache.CachedSession()
        if args.clear_cache:
            session.cache.clear()
        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)
        if results is not None:
            control_output(results, args)
    except Exception:
        logging.exception('Ошибка при выполнении', stack_info=True)
    logging.info('Парсер завершил работу')


if __name__ == '__main__':
    main()
