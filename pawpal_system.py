from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum


class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

    @property
    def order(self) -> int:
        return {"high": 0, "medium": 1, "low": 2}[self.value]


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
        """Append a task to this pet's task list."""
        self.tasks.append(task)


@dataclass
class Owner:
    name: str
    available_minutes: int
    day_start_hour: int
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def all_tasks(self) -> list[Task]:
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet):
        self.owner = owner
        self.pet = pet

    def add_task(self, task: Task) -> None:
        self.pet.add_task(task)

    def remove_task(self, task_name: str) -> None:
        self.pet.tasks = [t for t in self.pet.tasks if t.name != task_name]

    def generate_plan(self) -> list[tuple[str, Task]]:
        sorted_tasks = sorted(
            self.pet.tasks,
            key=lambda t: (t.priority.order, t.time),
        )

        plan: list[tuple[str, Task]] = []
        minutes_used = 0
        current_hour = self.owner.day_start_hour
        current_minute = 0

        for task in sorted_tasks:
            if minutes_used + task.duration_minutes > self.owner.available_minutes:
                continue

            slot = f"{current_hour:02d}:{current_minute:02d}"
            plan.append((slot, task))

            minutes_used += task.duration_minutes
            current_minute += task.duration_minutes
            current_hour += current_minute // 60
            current_minute = current_minute % 60

        return plan

    def explain(self) -> str:
        plan = self.generate_plan()
        if not plan:
            return "No tasks could be scheduled within the available time."

        lines = [
            f"Daily plan for {self.pet.name} ({self.pet.breed}):",
            f"  Owner: {self.owner.name} | Available: {self.owner.available_minutes} min\n",
        ]

        total_minutes = 0
        for slot, task in plan:
            priority_label = task.priority.value.upper()
            lines.append(
                f"  {slot} — {task.name} ({task.duration_minutes} min)"
                f" [{priority_label}]"
                + (f" — {task.notes}" if task.notes else "")
            )
            total_minutes += task.duration_minutes

        skipped = [
            t for t in self.pet.tasks
            if not any(t is task for _, task in plan)
        ]

        lines.append(f"\n  Total scheduled: {total_minutes} min")
        if skipped:
            skipped_names = ", ".join(t.name for t in skipped)
            lines.append(f"  Skipped (time ran out): {skipped_names}")

        return "\n".join(lines)
