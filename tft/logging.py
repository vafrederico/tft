from logging import Filter, LogRecord
from typing import Callable

class CustomLambdaFilter(Filter):
    fn: Callable

    def __init__(self, obj = None, fn: Callable = None) -> None:
        self.fn = fn
        self.obj = obj
        super().__init__()

    def filter(self, record: LogRecord) -> bool:
        if self.fn:
            record.lambda_field = self.fn()
        elif self.obj:
            record.lambda_field = str(self.obj)
        return True