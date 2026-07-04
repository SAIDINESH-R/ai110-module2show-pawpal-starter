from datetime import date

from pawpal_system import Owner, Pet, Task, Scheduler, Priority


def make_scheduler(available_minutes=120, day_start_hour=8):
    """Helper: owner with one dog named Biscuit."""
    owner = Owner(name="Alex", available_minutes=available_minutes, day_start_hour=day_start_hour)
    pet = Pet(name="Biscuit", species="dog", breed="Lab", age_years=2.0)
    owner.add_pet(pet)
    return Scheduler(owner=owner), pet


def test_add_task_increases_count():
    pet = Pet(name="Biscuit", species="dog", breed="Golden Retriever", age_years=3.0)
    task = Task(name="Morning Walk", duration_minutes=30, priority=Priority.HIGH, category="exercise")

    assert len(pet.tasks) == 0
    pet.add_task(task)
    assert len(pet.tasks) == 1


def test_task_completed_can_be_set():
    task = Task(name="Feeding", duration_minutes=10, priority=Priority.HIGH, category="nutrition")

    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_overbooked_skips_low_priority_first():
    scheduler, pet = make_scheduler(available_minutes=20)

    scheduler.add_task(Task("Walk", 15, Priority.HIGH, "exercise"), pet)
    scheduler.add_task(Task("Grooming", 15, Priority.LOW, "grooming"), pet)

    plan = scheduler.generate_plan()
    scheduled_names = [task.name for _, task in plan]

    assert "Walk" in scheduled_names
    assert "Grooming" not in scheduled_names


def test_completed_once_task_excluded_from_plan():
    scheduler, pet = make_scheduler()

    task = Task("Vet visit", 60, Priority.HIGH, "health", completed=True)
    scheduler.add_task(task, pet)

    plan = scheduler.generate_plan()
    assert len(plan) == 0


def test_weekly_task_only_due_on_correct_day():
    task = Task("Bath", 20, Priority.MEDIUM, "grooming",
                frequency="weekly", repeat_day=0)  # Monday

    monday = date(2025, 6, 2)
    tuesday = date(2025, 6, 3)

    assert task.is_due_today(monday) is True
    assert task.is_due_today(tuesday) is False


def test_time_slots_roll_over_hour_boundary():
    scheduler, pet = make_scheduler()

    scheduler.add_task(Task("Task A", 55, Priority.HIGH, "exercise", time="08:00"), pet)
    scheduler.add_task(Task("Task B", 10, Priority.HIGH, "health", time="09:00"), pet)

    plan = scheduler.generate_plan()
    slots = [slot for slot, _ in plan]

    assert slots[0] == "08:00"
    assert slots[1] == "08:55"


def test_conflicts_detects_overlapping_tasks():
    scheduler, pet = make_scheduler()

    task_a = Task("Walk", 30, Priority.HIGH, "exercise")
    task_b = Task("Feeding", 10, Priority.HIGH, "nutrition")

    fake_plan = [("08:00", task_a), ("08:10", task_b)]

    warnings = scheduler.conflicts(fake_plan)

    assert len(warnings) == 1
    assert "Walk" in warnings[0]
    assert "Feeding" in warnings[0]
    assert "CONFLICT" in warnings[0]
