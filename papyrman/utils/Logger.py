import logging
import colorlog


class Logger:
    def __init__(self, level, terminal_output):
        self.logger = logging.getLogger('papyrman')
        self.logger.setLevel(logging.DEBUG)

        self.file_handler = logging.FileHandler('logs.txt')
        self.file_handler.setLevel(level)

        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setLevel(terminal_output)

        # ToDo: create Logger_message accordance Level

        self.formatter_file = self.form(level, colored=False)
        self.formatter_terminal = self.form(terminal_output)
        self.file_handler.setFormatter(self.formatter_file)
        self.stream_handler.setFormatter(self.formatter_terminal)

        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.stream_handler)

        self.logger.info(f"Set File-Log Level to {level}")
        self.logger.info(f"Set Terminal-Log Level to {terminal_output}")

    @staticmethod
    def form(level, colored=True):
        log_colors = {
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
        if colored:
            start_color = "%(log_color)s"
            reset_color = "%(reset)s"
        else:
            start_color = ""
            reset_color = ""

        if level == 10:  # debug
            formatter = colorlog.ColoredFormatter(
                "%(asctime)s |" + start_color + " %(levelname)s" + reset_color + " |"
                "\n\t| Thread-ID: %(thread)d | Thread-Name: %(threadName)s"
                "\n\t| Process-ID: %(process)s | Process-Name: %(processName)s"
                "\n\t| File: %(filename)s | Line: %(lineno)d"
                "\n\t| %(module)s.%(funcName)s()"
                "\n\t| %(message)s"
                "\n\t| %(exc_info)s"
                "\n\t|",
                reset=False, log_colors=log_colors
            )
            return formatter
        else:  # info / warning / error / critical
            formatter = colorlog.ColoredFormatter(
                start_color + "\t%(levelname)s" + reset_color + " | %(message)s",
                reset=False, log_colors=log_colors
            )
            return formatter
