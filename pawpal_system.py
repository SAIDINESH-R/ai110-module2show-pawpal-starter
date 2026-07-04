from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, time as Time
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
    repeat_day: int = -1  # 0=Mon … 6=Sun, -1=not set

    def is_due_today(self, today: date | None = None) -> bool:
        """Return True if this task should appear in today's schedule."""
        weekday = (today or date.today()).weekday()
        if self.frequency == "daily":
            return True
        if self.frequency == "once":
            return not self.completed
        if self.frequency == "weekly":
            return self.repeat_day == weekday
        return False


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
        """Append a pet to this owner's pet list."""
        self.pets.append(pet)

    def all_tasks(self) -> list[Task]:
        """Return a flat list of every task across all owned pets."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def _all_tasks(self) -> list[Task]:
        """Return every task across all of the owner's pets."""
        return [task for pet in self.owner.pets for task in pet.tasks]

    def add_task(self, task: Task, pet: Pet) -> None:
        """Add a task to a specific pet's task list."""
        pet.add_task(task)

    def remove_task(self, task_name: str, pet: Pet) -> None:
        """Remove a task by name from a specific pet's task list."""
        pet.tasks = [t for t in pet.tasks if t.name != task_name]

    def tasks_by_category(self, category: str) -> list[Task]:
        """Return all tasks across all pets that match the given category."""
        return [t for t in self._all_tasks() if t.category == category]

    def is_overbooked(self) -> bool:
        """Return True if total pending task time across all pets exceeds available minutes."""
        total = sum(t.duration_minutes for t in self._all_tasks() if not t.completed)
        return total > self.owner.available_minutes

    def generate_plan(self, today: date | None = None) -> list[tuple[str, Task]]:
        """Sort due tasks across all pets by priority, time, and duration; fit within available minutes."""
        pending = [t for t in self._all_tasks() if t.is_due_today(today)]
        sorted_tasks = sorted(
            pending,
            key=lambda t: (t.priority.order, Time.fromisoformat(t.time), t.duration_minutes),
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

    def conflicts(self, plan: list[tuple[str, Task]]) -> list[str]:
        """Return warning strings for any two scheduled tasks whose time slots overlap."""
        def to_minutes(slot: str) -> int:
            h, m = slot.split(":")
            return int(h) * 60 + int(m)

        warnings = []
        for i, (slot_a, task_a) in enumerate(plan):
            end_a = to_minutes(slot_a) + task_a.duration_minutes
            for slot_b, task_b in plan[i + 1:]:
                if to_minutes(slot_b) < end_a:
                    warnings.append(
                        f"CONFLICT: {task_a.name} and {task_b.name} overlap at {slot_b}"
                    )
        return warnings

    def explain(self, today: date | None = None) -> str:
        """Return a human-readable summary of the combined plan across all pets."""
        plan = self.generate_plan(today)
        if not plan:
            return "No tasks could be scheduled within the available time."

        pet_names = ", ".join(p.name for p in self.owner.pets)
        lines = [
            f"Daily plan for {self.owner.name}'s pets ({pet_names}):",
            f"  Available: {self.owner.available_minutes} min\n",
        ]

        total_minutes = 0
        scheduled_ids = {id(task) for _, task in plan}
        for slot, task in plan:
            priority_label = task.priority.value.upper()
            pet_label = next(
                (p.name for p in self.owner.pets if task in p.tasks), "?"
            )
            lines.append(
                f"  {slot} — [{pet_label}] {task.name} ({task.duration_minutes} min)"
                f" [{priority_label}]"
                + (f" — {task.notes}" if task.notes else "")
            )
            total_minutes += task.duration_minutes

        skipped = [t for t in self._all_tasks() if id(t) not in scheduled_ids]

        lines.append(f"\n  Total scheduled: {total_minutes} min")
        if skipped:
            skipped_names = ", ".join(t.name for t in skipped)
            lines.append(f"  Skipped (time ran out or not due): {skipped_names}")

        return "\n".join(lines)
