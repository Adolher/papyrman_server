import logging


class Logger:
    def __init__(self, level, terminal_output):
        self.logger = logging.getLogger('papyrman')
        self.logger.setLevel(logging.DEBUG)

        self.file_handler = logging.FileHandler('logs.txt')
        self.file_handler.setLevel(level)

        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setLevel(terminal_output)

        # ToDo: create Logger_message accordance Level

        self.formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s |"
            "\n\t| Thread-ID: %(thread)d | Thread-Name: %(threadName)s"
            "\n\t| Process-ID: %(process)s | Process-Name: %(processName)s"
            "\n\t| File: %(filename)s | Line: %(lineno)d"
            "\n\t| %(module)s.%(funcName)s(%(message)s) |"
            "\n\t| %(exc_info)s"
            "\n\t|")
        self.file_handler.setFormatter(self.formatter)
        self.stream_handler.setFormatter(self.formatter)

        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.stream_handler)

        self.logger.info(f"[Set File-Logger to Level {level}]")
        self.logger.info(f"Set Terminal-Output to Level {terminal_output}")
