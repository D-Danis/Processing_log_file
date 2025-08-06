import pytest
import json
import tempfile
import os
from log_processor import LogProcessor
from errors import (
    FileReadError,
    JSONParseError,
    DataProcessingError,
    UnknownReportTypeError,
)

# Общий лог-контент для всех тестов
COMMON_LOG_CONTENT = "\n".join([
    json.dumps({"@timestamp": "2025-06-22T12:00:00", "url": "/api/v1/users", "response_time": 0.1, "http_user_agent": "UA1"}),
    json.dumps({"@timestamp": "2025-06-22T12:05:00", "url": "/api/v1/users", "response_time": 0.200, "http_user_agent": "UA2"}),
    json.dumps({"@timestamp": "2025-06-22T12:10:00", "url": "/api/v1/orders", "response_time": 0.300, "http_user_agent": "UA1"}),
])

# Вспомогательная функция для создания файла с общим контентом
def create_temp_log_file(contents=COMMON_LOG_CONTENT):
    tmp = tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8')
    tmp.write(contents)
    tmp.close()
    return tmp.name

# Тест успешного чтения и генерации отчета для типа 'average'
def test_generate_average_report():
    filename = create_temp_log_file()
    
    processor = LogProcessor(filename, report_type='average', date_filter='2025-06-22')
    processor.read_log()
    headers, report_rows = processor.get_report()

    # Проверка заголовков
    assert headers == ['Endpoint', 'Number of Requests', 'Average Response Time (s)']
    
    # Проверка данных
    expected = {
        "/api/v1/users": {'count': 2, 'total_time': 0.1 + 0.200},
        "/api/v1/orders": {'count': 1, 'total_time': 0.300}
    }
    
    for row in report_rows:
        endpoint = row[0]
        count = row[1]
        avg_time = float(row[2])
        assert endpoint in expected
        assert count == expected[endpoint]['count']
        expected_avg = expected[endpoint]['total_time'] / count
        assert abs(avg_time - expected_avg) < 1e-6

    os.remove(filename)

# Тест успешного отчета по количеству запросов
def test_generate_count_report():
    filename = create_temp_log_file()
    
    processor = LogProcessor(filename, report_type='count', date_filter='2025-06-22')
    processor.read_log()
    headers, report_rows = processor.get_report()

    assert headers == ['Endpoint', 'Number of Requests']
    
    counts = {row[0]: row[1] for row in report_rows}
    
    assert counts["/api/v1/users"] == 2
    assert counts["/api/v1/orders"] == 1

    os.remove(filename)

# Тест отчета по User-Agent
def test_generate_user_agent_report():
    filename = create_temp_log_file()
    processor = LogProcessor(filename, report_type='user_agent', date_filter='2025-06-22')
    processor.read_log()
    
    headers, report_rows = processor.get_report()
    assert headers == ['User-Agent', 'Count']
    
    ua_counts = {row[0]: row[1] for row in report_rows}
    assert ua_counts["UA1"] == 2
    assert ua_counts["UA2"] == 1
    
    os.remove(filename)

# Тест обработки файла не найден
def test_file_not_found():
    with pytest.raises(FileReadError):
        processor = LogProcessor("nonexistent_file.log")
        processor.read_log()

# Тест обработки отсутствия обязательных полей (например, отсутствует @timestamp или url)
def test_missing_fields():
     content_missing_timestamp = json.dumps({"url":"test_url","response_time":0.1})
     content_missing_url = json.dumps({"@timestamp":"2025-06-22T12:00:00","response_time":0.1})
     
     filename_ts_missing = create_temp_log_file(content_missing_timestamp)
     filename_url_missing= create_temp_log_file(content_missing_url)
     
     # Ожидаем DataProcessingError при отсутствии обязательных полей
     with pytest.raises(DataProcessingError):
         processor = LogProcessor(filename_ts_missing)
         processor.read_log()
         
     with pytest.raises(DataProcessingError):
         processor = LogProcessor(filename_url_missing)
         processor.read_log()

     os.remove(filename_ts_missing)
     os.remove(filename_url_missing)

# Тест неизвестного типа отчета вызывает исключение (уже есть в вашем коде)
def test_unknown_report_type():
     filename = create_temp_log_file()
     
     with pytest.raises(UnknownReportTypeError):
         processor = LogProcessor(filename, report_type='unknown_type')
         processor.read_log()
         
     os.remove(filename)


# Тест пустого файла (должен выбросить ошибку или вернуть пустой отчет)
def test_empty_file():
    filename = create_temp_log_file(contents="")
    
    # Предположим, что при пустом файле возвращается пустой отчет без ошибок.
    # Или можно проверить исключение в зависимости от реализации.
    
   # Если ваш код возвращает пустой отчет:
    processor = LogProcessor(filename)
    try:
        processor.read_log()
        headers, rows = processor.get_report()
        assert rows == []
    except Exception as e:
        pytest.fail(f"Unexpected exception for пустого файла: {e}")

    os.remove(filename)

# Тест файла с корректными и некорректными строками (должен пропускать плохие строки и читать хорошие)
def test_mixed_valid_invalid_lines():
    valid_data = {"@timestamp": "2025-06-22T12:00:00", "url": "/a", "response_time": 0.1}
    valid_line = json.dumps(valid_data)
    invalid_line = "{ invalid json }"
    content= "\n".join([valid_line, invalid_line])
    filename= create_temp_log_file(content)
     
    try:
        processor= LogProcessor(filename)
        processor.read_log()
        headers, rows=processor.get_report()
        # Проверяем что есть хотя бы одна строка с правильными данными
        assert len(rows) >= 1
         
        first_row = rows[0]
        assert first_row[0] == valid_data["url"]
            
    except Exception as e:
        pytest.fail(f"Unexpected exception при смешанных строках: {e}")
        
    finally:
        os.remove(filename)
