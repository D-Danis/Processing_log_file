class LogProcessingError(Exception):
    """Базовая ошибка при обработке логов."""
    pass

class FileReadError(LogProcessingError):
    """Ошибка при чтении файла."""
    pass

class JSONParseError(LogProcessingError):
    """Ошибка парсинга JSON."""
    pass

class DataProcessingError(LogProcessingError):
    """Ошибка при обработке данных."""
    pass

class UnknownReportTypeError(LogProcessingError):
    """Неизвестный тип отчета."""
    pass