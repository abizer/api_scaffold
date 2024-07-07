import logging
import inspect
import os
import uvicorn.logging
from functools import partial


def _get_calling_module(x=False) -> str:
    stack = inspect.stack()
    if len(stack) < 3:
        return ""
    caller_frame = stack[2]
    if x:
        for frame in stack:
            print(frame.frame)
    module = inspect.getmodule(caller_frame[0])
    relpath = caller_frame[0].f_code.co_filename.replace(f"{os.getcwd()}/", "")
    lineno = caller_frame[0].f_lineno
    funcname = caller_frame[0].f_code.co_name
    return (module.__name__ if module else "", relpath, lineno, funcname)


# uvicorn.logging.DefaultFormatter adds colors
class ColorizedFormatter(uvicorn.logging.DefaultFormatter):
    def format(self, record: logging.LogRecord) -> str:
        _r = record.__dict__.copy()
        for k, v in _r.items():
            if k.startswith("__"):
                record.__dict__[k[2:]] = v
                del record.__dict__[k]
        return super().format(record)


def make_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # don't redundantly add the same handler
    handler_exists = any(
        isinstance(handler, logging.StreamHandler)
        and handler.formatter.__class__ == ColorizedFormatter
        for handler in logger.handlers
    )
    if not handler_exists:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)

        formatter = ColorizedFormatter(
            "%(levelprefix)s %(pathname)s:%(lineno)d %(funcName)s - %(message)s"
        )
        stream_handler.setFormatter(formatter)

        logger.addHandler(stream_handler)

    return logger


def _log(level, *args, **kwargs):
    m, p, l, f = _get_calling_module()
    kwargs["extra"] = {
        "__module": m,
        "__pathname": p,
        "__lineno": l,
        "__funcName": f,
    }
    return logging.getLogger(m).log(level, *args, **kwargs)


L = partial(_log, logging.INFO)
D = partial(_log, logging.DEBUG)
