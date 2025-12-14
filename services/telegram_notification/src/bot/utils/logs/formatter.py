import logging


COLORED_LEVELS = {
    logging.DEBUG: "\033[36mDEBUG\033[0m",
    logging.INFO: "\033[32mINFO\033[0m",
    logging.WARNING: "\033[33mWARNING\033[0m",
    logging.ERROR: "\033[31mERROR\033[0m",
    logging.CRITICAL: "\033[91mCRITICAL\033[0m",
}


class ColorFormatter(logging.Formatter):
    def formatMessage(self, record: logging.LogRecord) -> str:
        field = COLORED_LEVELS.get(record.levelno, record.levelname)
        record.levelname = field + (" " * (17 - len(field)))

        return super().formatMessage(record)
