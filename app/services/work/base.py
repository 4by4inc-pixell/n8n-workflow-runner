from abc import ABC, abstractmethod
from models.n8n import N8NTaskRead


class WorkBase(ABC):
    def __init__(self, task: N8NTaskRead):
        self.task = task

    @property
    def labels(self) -> list[str]:
        return self.task.labels

    @property
    def task_type(self) -> str:
        return self.task.task_type

    @property
    def params(self) -> dict:
        return self.task.params

    @abstractmethod
    def execute(self) -> str:
        pass

    def __call__(self):
        return self.execute()
