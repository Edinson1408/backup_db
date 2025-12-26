from abc import ABC, abstractmethod


class DatabaseBackup(ABC):

    def __init__(self, config):
        self.config = config

    @abstractmethod
    def dump(self, output_file: str):
        pass

    @abstractmethod
    def filename(self) -> str:
        pass
