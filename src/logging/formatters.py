import json, logging

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "level": record.levelname,
            "msg": record.getMessage(),
            "logger": record.name,
            "time": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
        }
        # общие поля, если переданы через `extra=...`
        for k in ("request_id", "user_id", "path", "method", "status", "code"):
            v = getattr(record, k, None)
            if v is not None:
                payload[k] = v
        details = getattr(record, "details", None)
        if isinstance(details, dict):
            payload["details"] = details
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)
