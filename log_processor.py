import json
from datetime import datetime
from collections import defaultdict

from errors import (
    FileReadError,
    DataProcessingError,
    UnknownReportTypeError,
)
from reports import (
    AverageResponseTimeReport, 
    CountRequestsReport, 
    UserAgentReport
)


class LogProcessor:
    REPORT_TYPES = {
        'average': AverageResponseTimeReport,
        'count': CountRequestsReport,
        'user_agent': UserAgentReport,
    }

    def __init__(self, file_path, report_type='average', date_filter=None):
        self.file_path = file_path
        self.report_type = report_type
        self.date_filter_str = date_filter  
        self.endpoints_data = defaultdict(lambda: {'count': 0, 'total_time': 0.0})
        self.entries_for_reports = []
        
        if self.report_type not in ['average', 'count', 'user_agent']:
            raise UnknownReportTypeError(f"Unknown report type: {self.report_type}")

    def read_log(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                for line_number, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        log_entry = json.loads(line)
                    except json.JSONDecodeError as e:
                        continue
                    if '@timestamp' not in log_entry or 'url' not in log_entry:
                        raise DataProcessingError(f"Некорректный формат даты в строке {line_number}")

                    # Фильтр по дате
                    if hasattr(self, 'date_filter_str') and self.date_filter_str:
                        timestamp_str = log_entry.get('@timestamp')
                        if not timestamp_str:
                            continue  
                        try:
                            timestamp_dt = datetime.fromisoformat(timestamp_str)
                            filter_date_dt = datetime.fromisoformat(self.date_filter_str)
                        except ValueError as e:
                            raise DataProcessingError(f"Некорректный формат даты в строке {line_number}: {e}")
                        if timestamp_dt.date() != filter_date_dt.date():
                            continue

                    self.entries_for_reports.append(log_entry)

                    url = log_entry.get('url')
                    response_time = log_entry.get('response_time')
                    if url is None or response_time is None:
                        raise DataProcessingError(f"Отсутствует 'url' или 'response_time' в строке {line_number}")
                    
                    self.endpoints_data[url]['count'] += 1
                    self.endpoints_data[url]['total_time'] += response_time

        except FileNotFoundError as e:
            raise FileReadError(f"Файл не найден: {self.file_path}")
        except IOError as e:
            raise FileReadError(f"Ошибка при чтении файла: {e}")

    def get_report(self):
        report_class = self.REPORT_TYPES.get(self.report_type)
        if not report_class:
            raise UnknownReportTypeError(f"Неизвестный тип отчета: {self.report_type}")
        
        if issubclass(report_class, UserAgentReport):
            return report_class(self.entries_for_reports).generate()
        else:
            return report_class(self.endpoints_data).generate()