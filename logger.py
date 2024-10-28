"""
This module is used to wrap the logging module with a singleton class.
Includes also class Cipher used to decrypt passwords
"""
import logging
import logging.config
from queue import Queue
from logging.handlers import QueueListener 
from base64 import b64decode

def singleton(cls):
    instances = {}
    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return get_instance()

@singleton
class Logger:
    """Wrapper and initilization of logging module with singleton"""
    logger:logging.Logger
    listener:QueueListener
    
    def __init__(self) -> None:
        self.listener:QueueListener = None 
        self.queue_log_from_ini()
    
    def queue_log_from_ini(s):
        """
        Configures logging from a configuration file named 'config-log.ini' and returns a logger.
        
        The function sets up a QueueListener to handle log messages and starts the listener.
        It then logs an error message with the text 'Test logging.' and stops the listener.
        
        Returns:
            Logger: A logger instance configured according to the 'config-log.ini' file.
        """
        logging.config.fileConfig("config-log.ini")
        s.logger = logging.getLogger("rcs_logger")
        s.listener = QueueListener(Queue(-1), s.logger.handlers)
        s.listener.start()

    def __del__(self):
        """stop QueueListener on class delete"""
        self.listener.stop()

class LoggerModule():
    """logger wrapper used by the modules to track position"""
    logger:Logger
    module_name:str = "main"

    def __init__(self, module_name:str):
        self.logger = Logger
        self.module_name = module_name.upper()
        
    def error(self, msg:str):
        self.logger.logger.error(f"{self.module_name} - {msg}")

    def debug(self, msg:str):
        self.logger.logger.debug(f"{self.module_name} - {msg}")

    def info(self, msg:str):
        self.logger.logger.info(f"{self.module_name} - {msg}")


