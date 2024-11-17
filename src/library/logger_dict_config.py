import colorlog

from src.library.dynamic_file_handler import DynamicFileHandler

# Define the logging configuration
logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simpleFormatter': {
            'format': '[%(asctime)s] - [%(levelname)s]: %(message)s',
            'datefmt': '%I:%M:%S %p',
        },
        'colorFormatter': {
            '()': colorlog.ColoredFormatter,  # Use colorlog's ColoredFormatter
            'format': '[%(asctime)s] - %(log_color)s[%(levelname)s]%(reset)s - %(message)s',
            'datefmt': '%Y-%m-%d %I:%M:%S %p',
            'log_colors': {
                'DEBUG': 'white',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white'
            }
        }
    },
    'handlers': {
        'fileHandler': {
            'class': DynamicFileHandler,
            'level': 'INFO',
            'formatter': 'simpleFormatter',
            'log_folder_name': '',
        },
        'archiveFileHandler': {
            'class': DynamicFileHandler,
            'level': 'INFO',
            'formatter': 'simpleFormatter',
            'log_folder_name': 'archive_logs',
        },
        'remotePCFileHandler': {
            'class': DynamicFileHandler,
            'level': 'INFO',
            'formatter': 'simpleFormatter',
            'log_folder_name': 'Remote_PC_logs',
        },
        'streamHandler': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'colorFormatter',
            # No args needed for StreamHandler
        },
    },
    'loggers': {
        # Root logger configuration
        'root': {
            'level': 'INFO',
            'handlers': ['fileHandler', 'streamHandler'],
        },
        # Archive logger configuration
        'archive': {
            'level': 'INFO',
            'handlers': ['archiveFileHandler', 'streamHandler'],
            # Propagate is set to False by default in dictConfig, so no need to specify it.
        },
        # Remote PC logger configuration
        'remotePC': {
            'level': 'INFO',
            'handlers': ['remotePCFileHandler', 'streamHandler'],
            # Propagate is set to False by default in dictConfig, so no need to specify it.
        },
    }
}
