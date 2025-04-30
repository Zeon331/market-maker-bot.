import logging
import json_log_formatter
from pythonjsonlogger import jsonlogger

class StructuredLogger:
    def __init__(self, name, level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        formatter = jsonlogger.JsonFormatter(
            '%(asctime)s %(levelname)s %(message)s %(module)s %(funcName)s'
        )
        
        # Консольный вывод
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        # Файловый вывод
        file_handler = logging.FileHandler('trader.log')
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def log(self, level, message, **kwargs):
        extra = {'context': kwargs}
        self.logger.log(level, message, extra=extra)

# Инициализация логгера
logger = StructuredLogger('SteamTrader', logging.DEBUG).logger