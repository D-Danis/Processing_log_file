# main.py
import argparse
from tabulate import tabulate
from log_processor import LogProcessor
from errors import (
    LogProcessingError,
)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Обработка лог-файла и формирование отчета.')
    parser.add_argument('--file', required=True, help='Путь к лог-файлу в формате JSON')
    parser.add_argument('--report', choices=['average', 'count', 'user_agent'], default='average',
                        help='Тип отчета: "average", "count", "user_agent"')
    parser.add_argument('--date', help='Фильтр по дате в формате ГГГГ-ММ-ДД (например: 2025-06-22)')
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    try:
        processor = LogProcessor(args.file, args.report, args.date)
        processor.read_log()
        
        headers, report_rows = processor.get_report()
        
        print(tabulate(report_rows, headers=headers, tablefmt='grid'))
        
    except LogProcessingError as e:
        print(f"Ошибка: {e}")

if __name__ == '__main__':
    main()