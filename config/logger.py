import logging


class Logger:
    """
    Logging engine.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        formatter = logging.Formatter(f'%(asctime)s [%(levelname)s] %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setLevel("INFO")
        console_handler.setFormatter(formatter)
        self.logger.setLevel("INFO")
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        self.logger.addHandler(console_handler)

    def get_log(self):
        """
        Get logger.

        :return: logger.
        """
        return self.logger