from logging import INFO, ERROR, Formatter, getLogger, Logger
from logging.handlers import TimedRotatingFileHandler


def get_info_logger() -> Logger:
    info_handler = TimedRotatingFileHandler(
        filename="./logs/info.log",
        when="midnight",
        backupCount=30,
        encoding="utf-8"
    )
    info_handler.setLevel(INFO)
    info_handler.setFormatter(Formatter("[%(asctime)s] [%(levelname)s | %(module)s] >>> %(message)s"))

    logger: Logger = getLogger("info")
    logger.setLevel(INFO)
    logger.addHandler(info_handler)

    return logger


def get_error_logger() -> Logger:
    error_handler = TimedRotatingFileHandler(
        filename="./logs/error.log",
        when="midnight",
        backupCount=6,
        encoding="utf-8"
    )
    error_handler.setLevel(ERROR)
    error_handler.setFormatter(Formatter("[%(asctime)s] [%(levelname)s | %(module)s] >>> %(message)s"))

    logger: Logger = getLogger("error")
    logger.setLevel(ERROR)
    logger.addHandler(error_handler)

    return logger
