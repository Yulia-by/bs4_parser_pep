# Парсер документации python и PEP

## Описание

Парсер информации о python с https://docs.python.org/3/ и https://peps.python.org/

Перед использованием
Клонируйте репозиторий к себе на компьютер при помощи команд:
```bash
git clone git@github.com:Yulia-by/bs4_parser_pep.git
```
В корневой папке создайте виртуальное окружение и установите зависимости:
```bash
python -m venv venv
pip install -r requirements.txt
```
Программа запускается из main.py в папке ./src/
```bash
python main.py [вариант парсера] [аргументы]
```
## Встроенные парсеры

- whats-new
Парсер выводящий спсок изменений в python.
```bash
python main.py whats-new [аргументы]
```
- latest_versions
Парсер выводящий список версий python и ссылки на их документацию.
```bash
python main.py latest-versions [аргументы]
```
- download
Парсер скачивающий zip архив с документацией python в pdf формате.
```bash
python main.py download [аргументы]
```
- pep
Парсер выводящий список статусов документов pep и количество документов в каждом статусе.
```bash
python main.py pep [аргументы]
```
## Аргументы

Есть возможность указывать аргументы для изменения работы программы:

- -h, --help Общая информация о командах.
```bash
python main.py -h
```
- -c, --clear-cache Очистка кеша перед выполнением парсинга.
```bash
python main.py [вариант парсера] -c
```
- -o {pretty,file}, --output {pretty,file}
Дополнительные способы вывода данных
pretty - выводит данные в командной строке в таблице
file - сохраняет информацию в формате csv в папке ./results/
```bash
python main.py [вариант парсера] -o file
```
Автор:
@Yulia-by