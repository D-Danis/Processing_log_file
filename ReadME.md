# Проект обработки лог-файлов

Этот проект предназначен для чтения, обработки и генерации отчетов из лог-файлов. В нем реализованы классы для парсинга логов, генерации различных отчетов и тесты для проверки корректности работы.

---

## Структура проекта

```
/processing_log_file
│
├── main.py                 # Точка входа
├── log_processor.py        # Основной код обработки логов
├── report.py               # Классы для генерации отчетов
├── errors.txt              # Классы для ошибок
├── test_log_processor.py   # Тесты с использованием pytest
├── requirements.txt        # Зависимости проекта
├── example1.log.txt        # Лог файл для проверки
└── README.md               # Этот файл
```

---

## Установка

1. Создайте виртуальное окружение (рекомендуется):

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
```

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

---
## Пример работы операции
- вывода среднего значение

```sh
python main.py --file example1.log --report average
```

- вывода количество

```sh
python main.py --file example1.log --report count
```

- вывода User Agent

```sh
python main.py --file example1.log --report user_agent
```

- возможность указать дату, чтобы сформировать отчет только по записям с указанной датой
```sh
python main.py --file example1.log --date 2025-06-22
```

- а также комбинировать 

```sh
python main.py --file example1.log --report user_agent --date 2025-06-22
```


## Запуск тестов

Для запуска всех тестов используйте команду:

```bash
pytest --maxfail=1 --disable-warnings -v
```

Это запустит все тесты и покажет их результаты.

```sh
pytest --maxfail=1 --disable-warnings -v
============================= test session starts =======================
platform linux -- Python 3.12.7, pytest-8.4.1, pluggy-1.6.0 -- */processing_log_file/.venv/bin/python3
cachedir: .pytest_cache
rootdir: */processing_log_file
plugins: cov-6.2.1
collected 8 items                                                              

test_log_processor.py::test_generate_average_report PASSED               [ 12%]
test_log_processor.py::test_generate_count_report PASSED                 [ 25%]
test_log_processor.py::test_generate_user_agent_report PASSED            [ 37%]
test_log_processor.py::test_file_not_found PASSED                        [ 50%]
test_log_processor.py::test_missing_fields PASSED                        [ 62%]
test_log_processor.py::test_unknown_report_type PASSED                   [ 75%]
test_log_processor.py::test_empty_file PASSED                            [ 87%]
test_log_processor.py::test_mixed_valid_invalid_lines PASSED             [100%]

============================== 8 passed in 0.02s ========================
```
---

## Проверка покрытия тестами

Для измерения покрытия кода используйте плагин `pytest-cov`. 

Запустите тесты с покрытием:

```bash
pytest --cov=log_processor --cov-report=term-missing:skip-covered
```

Результат
```sh
============================= test session starts =====================
platform linux -- Python 3.12.7, pytest-8.4.1, pluggy-1.6.0
rootdir: */processing_log_file
plugins: cov-6.2.1
collected 8 items                                                              

test_log_processor.py ........                                           [100%]

================================ tests ======================
_______________ coverage: platform linux, python 3.12.7-final-0 ________________

Name               Stmts   Miss  Cover   Missing
------------------------------------------------
log_processor.py      57      8    86%   36, 51, 55-56, 58, 66, 74, 79
------------------------------------------------
TOTAL                 57      8    86%
============================== 8 passed in 0.06s ============
```