import logging
import time
from collections.abc import Callable
from logging import Formatter

import orjson
from loguru import logger

_LEVEL_TO_LOWER_NAME = {
    logging.CRITICAL: "fatal",
    logging.ERROR: "error",
    logging.WARNING: "warn",
    logging.INFO: "info",
    logging.DEBUG: "debug",
}


class JsonFormatter(Formatter):  # pragma: no cover
    def __init__(self, time_format: str = "seconds"):
        super().__init__()

        if time_format == "seconds":
            self._convert_time: Callable = self._seconds
        else:
            self._convert_time = self._iso8601

    @staticmethod
    def _seconds(record: logging.LogRecord) -> float:
        return record.created

    @staticmethod
    def _iso8601(record: logging.LogRecord) -> str:
        return (
            time.strftime("%Y-%m-%dT%H:%M:%S.%%03d%z", time.localtime(record.created))
            % record.msecs
        )

    def format(self, record: logging.LogRecord):
        msg_dict = {
            "level": _LEVEL_TO_LOWER_NAME[record.levelno],
            "time": self._convert_time(record),
            "caller": "/".join(record.pathname.split("/")[-2:]) + f":{record.lineno}",
            "msg": record.msg,
        }

        # Since only loguru is used, all additional data is written to extra.
        # The task of extracting that data to the outer depth
        for k, v in record.__dict__.get("extra", {}).items():
            msg_dict[k] = v

        return orjson.dumps(msg_dict).decode()


logging.logThreads = False
logging.logMultiprocessing = False
logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("s3transfer").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)


def set_logger(json_format: bool = True):
    logger.remove()
    if json_format:
        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter(time_format="seconds"))
        logger.add(
            handler,
            format="{message}",
            level=logging.INFO,
        )
    else:
        import sys

        logger.add(
            sys.stderr,
            format="<level>{level: <8}</level>"
            " | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>"
            " - <level>{message}</level>"
            " - <level>{extra}</level>",
            level=logging.NOTSET,
        )
