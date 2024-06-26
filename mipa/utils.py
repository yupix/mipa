import logging
import re
from typing import Any, Literal

LOGING_LEVEL_TYPE = Literal[
    "NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
]
LOGING_LEVELS = {
    "NOTSET": 0,
    "DEBUG": 10,
    "INFO": 20,
    "WARNING": 30,
    "ERROR": 40,
    "CRITICAL": 50,
}


class _MissingSentinel:
    def __eq__(self, other):
        return False

    def __bool__(self):
        return False

    def __repr__(self):
        return "..."


MISSING: Any = _MissingSentinel()


def str_lower(text: str):
    pattern = re.compile("[A-Z]")
    large = [i.group().lower() for i in pattern.finditer(text)]
    result: list[Any | str] = [None] * (len(large + pattern.split(text)))
    result[::2] = pattern.split(text)
    result[1::2] = ["_" + i.lower() for i in large]
    return "".join(result)


def parse_logging_level(level: LOGING_LEVEL_TYPE):
    if level in LOGING_LEVELS:
        return LOGING_LEVELS[level]
    raise Exception("Not found logging level {0}" % (level))


def setup_logging(
    *,
    handler: logging.Handler | None = None,
    formatter: logging.Formatter | None = None,
    level: LOGING_LEVEL_TYPE = "INFO",
) -> None:
    _level = parse_logging_level(level)

    if _level is None:
        _level = logging.INFO

    if handler is None:
        handler = logging.StreamHandler()

    if formatter is None:
        # if isinstance(handler, logging.StreamHandler): TODO: カラー出力に対応する
        #     pass
        # else:
        dt_fmt = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(
            "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
        )

    logger = logging.getLogger()

    handler.setFormatter(formatter)
    logger.setLevel(_level)
    logger.addHandler(handler)
