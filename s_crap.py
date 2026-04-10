#!/usr/bin/env python3
from seleniumbase import SB
import argparse
import logging
import signal
import sys

url = 'https://checko.ru/search/advanced'  # ?page={1,500}


def parse_company_urls(page):
    cur_url = url + '?page=' + str(page)
    urls = []
    try:
        with SB(uc=True, headless=True) as sb:
            sb.activate_cdp_mode(cur_url)
            logging.info("Начинаем поиск url в %s" % cur_url)

            links = sb.find_elements("a.link")
            if links:
                for link in links:
                    link_href = link.get_attribute("href")
                    if "company" in link_href:
                        logging.info("Найдена ссылка %s" % link_href)
                        urls.append(link_href)
            else:
                logging.warning("Ссылки на найдены")
    except Exception as err:
        logging.error("Вызвано исключение:", exc_info=True)
    logging.info("Поиск url в %s окончен" % cur_url)
    return urls


# Столбцы:
# inn | address | main_okved | main_descr | add_okveds | add_descrs
def parse_company_data(comp_url):
    comp_str = ''
    try:
        with SB(uc=True, headless=True) as sb:
            sb.activate_cdp_mode(comp_url)
            logging.info("Начинаем парсить %s" % comp_url)

            inn = sb.find_element("#copy-inn")
            if inn is not None:
                comp_str += inn.text + ';'
            else:
                logging.warning("ИНН не найден")

            addr = sb.find_element("#copy-address")
            if addr is not None:
                comp_str += addr.text + ';'
            else:
                logging.warning("Юр.адрес не найден")

            add_okveds = ''
            add_descrs = ''
            rows = sb.find_elements("section#activity table tr")
            if rows:
                for i, row in enumerate(rows):
                    okved, descr = row.text.split(' ', 1)
                    if i == 0:
                        comp_str += okved + ';' + descr + ';'
                    else:
                        add_okveds += okved + '|'
                        add_descrs += descr + '|'
            else:
                logging.warning("Таблица с видами деятельности не найдена")

            if add_okveds:
                comp_str += add_okveds[:-1] + ';'
            if add_descrs:
                comp_str += add_descrs[:-1]
    except Exception as err:
        logging.error("Вызвано исключение:", exc_info=True)
    if not comp_str:
        logging.warning("Не получилось спарсить данные с %s" % comp_url)
    else:
        logging.info("Парсинг %s завершен" % comp_url)
    return comp_str


def set_up_argparser():
    parser = argparse.ArgumentParser(
        prog = "s_crap.py",
        description = "parses companies data"
    )
    parser.add_argument('-f', '--file', default=None,
                        help='file to write logs to, default is stdout')
    parser.add_argument('-l', '--log-level', 
                        choices=['NOTSET', 'DEBUG', 'INFO',
                                 'WARNING', 'ERROR', 'CRITICAL'],
                        default='INFO',
                        help='set logging level, default is INFO')
    return parser


def set_up_logging(file, log_level):
    match log_level:
        case 'NOTSET':
            level = logging.NOTSET
        case 'DEBUG':
            level = logging.DEBUG
        case 'INFO':
            level = logging.INFO
        case 'WARNING':
            level = logging.WARNING
        case 'ERROR':
            level = logging.ERROR
        case 'CRITICAL':
            level = logging.CRITICAL
    logging.basicConfig(level=level, filename=file, filemode='a',
                        format='%(asctime)s %(levelname)s %(message)s')


def sigint_hdl(signo, frame):
    sys.exit(1)


def main():
    parser = set_up_argparser()
    args = parser.parse_args()
    set_up_logging(args.file, args.log_level)
    f = open('../Downloads/data.csv', 'a', buffering=1)
    n = 0
    for page in range(1, 501):
    # for page in range(474, 439, -1):  # 60 pages, 60*25=1500 companies ~ 3h
        urls = parse_company_urls(page)
        for comp_url in urls:
            comp_str = parse_company_data(comp_url)
            if comp_str:
                f.write(comp_str + '\n')
                n += 1
                logging.info("В файл записана следующая строка:\n%s" %
                             comp_str)
                logging.info("Строк прочитано: %d" % n)
    f.close()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint_hdl)
    main()
