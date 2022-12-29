import abc
import backoff
import json

from core.config import settings


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        pass

    @abc.abstractmethod
    def load_state(self) -> dict:
        pass


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: str = None):
        self.file_path = file_path

    def save_state(self, state: dict) -> None:
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(state, file, sort_keys=False, indent=4)

    def load_state(self) -> dict:
        with open(self.file_path, 'r', encoding='utf-8') as file:
            try:
                return json.load(file)
            except:
                return {}


class State:
    def __init__(self, storage: BaseStorage):
        self.storage = storage

    @backoff.on_exception(
        wait_gen=backoff.expo,
        exception=(RuntimeError, ConnectionError, TimeoutError),
        max_time=settings.backoff_timeout,
    )
    def set_state(self, value: any) -> None:
        self.storage.save_state(value)

    @backoff.on_exception(
        wait_gen=backoff.expo,
        exception=(RuntimeError, ConnectionError, TimeoutError),
        max_time=settings.backoff_timeout,
    )
    def get_state(self, key: str) -> any:
        if key in self.storage.load_state():
            return self.storage.load_state()[key]
        else:
            return None
