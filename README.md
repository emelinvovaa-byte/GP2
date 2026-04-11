# GP2

В файле `s_crap.py` содержится скрипт парсер, использующий библиотеку
`SeleniumBase` для получения данных из html. Скрипт позволяет передавать
через флаги настройки для логирования (уровень логирования и файл для
логов): 

```
usage: python3 s_crap.py [-h] [-f FILE] [-l {NOTSET,DEBUG,INFO,WARNING,ERROR,CRITICAL}]

parses companies data

options:
  -h, --help            show this help message and exit
  -f, --file FILE       file to write logs to, default is stdout
  -l, --log-level {NOTSET,DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        set logging level, default is INFO
```

В файле `API_and_merging.ipynb` производится получение данных с помощью
API, а также объединение датасетов, полученных после скрапинга и API

## Данные

Данные для скрапинга взяты с сайта 'https://checko.ru/search/advanced'.
Использовался API: 'https://api-fns.ru/api/multinfo'.
Датасет представляет из себя данные о российских компаниях.


inn - ИНН

address - Юр.Адрес

main_okved - ОКВЭД основной деятельности

main_descr - текстовое описание основной деятельности

add_okveds - ОКВЭД дополнительных деятельностей (разделённых символом '|')

add_descrs - текст. описания дополнительных деятельностей (разделённых
символом '|')

КПП - Код причины постановки на учёт

ОГРН - Основной государственный регистрационный номер

ДатаОГРН - Дата получения ОГРН

ДатаРег - Дата Регистрации компании

Статус - нынешний статуc компании

Капитал - Уставной капитал компании

НаимПолнЮЛ - Полное наименование компании

