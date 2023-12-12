import datetime
import logging

class Logger:
    Error = 0
    Warn = 1
    Info = 2
    Debug = 3
    Critical = 4

    COLORS = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'reset': '\033[0m',
    }

    ELEMENT_COLORS = {
        'datetime': 'magenta',
        'level': {
            Error: 'red',
            Warn: 'yellow',
            Info: 'green',
            Debug: 'cyan',
            Critical: 'red',  # Critical is set to red
        },
        'message': 'white',
    }

    def __init__(self, file_name, verbose_level=Warn):
        self.file_name = file_name
        self.verbose_level = verbose_level
        self.log_queue = []

        self.configure_logging()

    def configure_logging(self, log_format=None, console_log_format=None, date_format=None):
        self.log_format = log_format or '{datetime}{level}{message}{reset}'
        self.console_log_format = console_log_format or '{datetime}{level}{message}{reset}'
        self.date_format = date_format or '%Y-%m-%d %H:%M:%S'

        # Configure file handler
        file_handler = logging.FileHandler(self.file_name)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(fmt=self.log_format, datefmt=self.date_format)
        file_handler.setFormatter(file_formatter)

        # Configure console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG if self.verbose_level == Logger.Debug else logging.WARNING)
        console_formatter = logging.Formatter(fmt=self.console_log_format, datefmt=self.date_format)
        console_handler.setFormatter(console_formatter)

        # Configure root logger
        logging.root.handlers = []  # Clear existing handlers to avoid duplicate logs
        logging.root.addHandler(file_handler)
        logging.root.addHandler(console_handler)

    def set_log_format(self, log_format):
        self.log_format = log_format
        self.configure_logging()

    def set_console_log_format(self, console_log_format):
        self.console_log_format = console_log_format
        self.configure_logging()

    def set_verbose_level(self, verbose_level):
        self.verbose_level = verbose_level

        # Update console handler level
        console_handler = next(handler for handler in logging.root.handlers if isinstance(handler, logging.StreamHandler))
        console_handler.setLevel(logging.DEBUG if self.verbose_level == Logger.Debug else logging.WARNING)

    def get_verbose_level(self):
        return self.verbose_level

    def colorize(self, text, color):
        return f'{self.COLORS[color]}{text}{self.COLORS["reset"]}'

    def format_log_entry(self, record):
        formatted_entry = self.log_format

        for element, color in self.ELEMENT_COLORS.items():
            if isinstance(color, dict):  # Handle level color mappings
                element_value = record.levelno
                color_mapping = color.get(element_value, 'white')
            else:
                color_mapping = color

            formatted_entry = formatted_entry.replace(f'{{{element}}}', self.colorize(str(getattr(record, element, '')), color_mapping))

        return formatted_entry

    def queue_log(self, level, message):
        self.log_queue.append({'level': level, 'message': message})

    def write_log(self, level, message):
        logger = logging.getLogger()
        record = logging.LogRecord(
            name='root',
            level=level,
            pathname='',
            lineno=0,
            msg=message,
            args=(),
            exc_info=None
        )
        formatted_entry = self.format_log_entry(record)
        logger.log(level, formatted_entry)

        if level >= Logger.Critical and self.verbose_level >= Logger.Critical:
            raise Exception("Critical error encountered.")  # Raise an exception instead of exiting

    def write_log_queue(self):
        for entry in self.log_queue:
            self.write_log(entry['level'], entry['message'])

        # Check if there are any critical errors in the queue before raising an exception
        if any(entry['level'] >= Logger.Critical for entry in self.log_queue):
            raise Exception("Critical error(s) encountered in log queue.")

    @staticmethod
    def generate_log_file_name(prefix, path=None, format_string=None):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
        format_string = format_string or '{prefix}_{timestamp}.log'

        log_file_name = format_string.format(prefix=prefix, timestamp=timestamp)

        if path:
            log_file_name = os.path.join(path, log_file_name)

        return log_file_name

# Example Usage:
# log_file_path = '/path/to/logs'
# log_file_name_format = '{prefix}_{timestamp}_%Y%m%d.log'

# log_file_name = Logger.generate_log_file_name('my_log', path=log_file_path, format_string=log_file_name_format)
# my_logger = Logger(log_file_name, verbose_level=Logger.Debug)

# Configure log format and console log format
# my_logger.configure_logging(log_format='%(asctime)s - %(levelname)s - %(message)s', date_format='%Y-%m-%d %H:%M:%S')

# Optionally, set a custom console log format
# my_logger.set_console_log_format('{asctime} - {levelname} - {message}')

# Change verbose level during runtime
# my_logger.set_verbose_level(Logger.Info)

# Check the current verbose level
# print(f"Current Verbose Level: {my_logger.get_verbose_level()}")

# Queue some log entries
# my_logger.queue_log(Logger.Warn, "This is a warning message.")
# my_logger.queue_log(Logger.Info, "This is an info message.")

# Write the log entries in the queue
# my_logger.write_log_queue()

