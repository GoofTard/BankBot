from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self, userId: str, commandLine: list) -> str:
        pass