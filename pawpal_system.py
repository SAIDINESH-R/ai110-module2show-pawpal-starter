from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum


class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Task:
    name: str
    duration_minutes: int
    priority: Priority
    category: str
    notes: str = ""
    time: str = "08:00"
    frequency: str = "once"
    completed: bool = False


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age_years: float
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass


@dataclass
class Owner:
    name: str
    available_minutes: int
    day_start_hour: int
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def all_tasks(self) -> list[Task]:
        pass


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet):
        self.owner = owner
        self.pet = pet
        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task_name: str) -> None:
        pass

    def generate_plan(self) -> list[tuple[str, Task]]:
        pass

    def explain(self) -> str:
        pass
