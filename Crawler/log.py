import logging.config
import logging
import os
import time

config = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': '[%(levelname)s]%(asctime)s  %(module)s/%(funcName)s : %(message)s',
        },
        # 其他的 formatter
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'Crawler/log/logging_' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.log',
            'level': 'DEBUG',
            'formatter': 'simple'
        },
        # 其他的 handler
    },
    'loggers': {
        'StreamLogger': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'FileLogger': {
            # 既有 console Handler，还有 file Handler
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
        # 其他的 Logger
    }
}

os.makedirs("Crawler/log", exist_ok=True)
logging.config.dictConfig(config)
StreamLogger = logging.getLogger("StreamLogger")
FileLogger = logging.getLogger("FileLogger")

if __name__ == '__main__':
    FileLogger.debug("test")
