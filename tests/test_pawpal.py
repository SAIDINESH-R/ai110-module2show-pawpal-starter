from pawpal_system import Pet, Task, Priority


def test_add_task_increases_count():
    pet = Pet(name="Biscuit", species="dog", breed="Golden Retriever", age_years=3.0)
    task = Task(name="Morning Walk", duration_minutes=30, priority=Priority.HIGH, category="exercise")

    assert len(pet.tasks) == 0
    pet.add_task(task)
    assert len(pet.tasks) == 1


def test_task_completed_can_be_set():
    task = Task(name="Feeding", duration_minutes=10, priority=Priority.HIGH, category="nutrition")

    assert task.completed is False
    task.completed = True
    assert task.completed is True
