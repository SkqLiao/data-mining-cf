import logging
from logging.handlers import RotatingFileHandler

class Logger:
    def __init__(self, file_path, level=logging.INFO, max_bytes=10485760, backup_count=5):
        self.logger = logging.getLogger()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        
        file_handler = RotatingFileHandler(file_path, maxBytes=max_bytes, backupCount=backup_count)
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)
        
        self.logger.setLevel(level)

    def __getattr__(self, name):
        def method(*args, **kwargs):
            attr = getattr(self.logger, name)
            if callable(attr):
                return attr(*args, **kwargs)
            return attr
        return method
