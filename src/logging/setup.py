import logging
from .formatters import JsonFormatter

def setup_logging(level: int = logging.INFO, *, uvicorn_tidy: bool = True) -> None:
    root = logging.getLogger()
    root.setLevel(level)

    h = logging.StreamHandler()
    h.setFormatter(JsonFormatter())
    root.handlers[:] = [h]   # заменить дефолтные

    if uvicorn_tidy:
        # сделаем uvicorn/uvicorn.access менее шумными или переведём на наш формат
        for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
            logging.getLogger(name).handlers[:] = []
            logging.getLogger(name).propagate = True  # пусть идут в root
