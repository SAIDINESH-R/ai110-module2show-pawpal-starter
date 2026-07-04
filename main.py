from pawpal_system import Owner, Pet, Task, Scheduler, Priority

owner = Owner(name="Alex", available_minutes=120, day_start_hour=8)

biscuit = Pet(name="Biscuit", species="dog", breed="Golden Retriever", age_years=3.0)
whiskers = Pet(name="Whiskers", species="cat", breed="Siamese", age_years=5.0)

owner.add_pet(biscuit)
owner.add_pet(whiskers)

# --- Biscuit's tasks ---
biscuit_scheduler = Scheduler(owner=owner, pet=biscuit)

biscuit_scheduler.add_task(Task(
    name="Morning Walk",
    duration_minutes=30,
    priority=Priority.HIGH,
    category="exercise",
    time="08:00",
    notes="go to the park",
))
biscuit_scheduler.add_task(Task(
    name="Feeding",
    duration_minutes=10,
    priority=Priority.HIGH,
    category="nutrition",
    time="08:30",
))
biscuit_scheduler.add_task(Task(
    name="Flea Medicine",
    duration_minutes=5,
    priority=Priority.MEDIUM,
    category="health",
    time="09:00",
    notes="apply between shoulder blades",
))
biscuit_scheduler.add_task(Task(
    name="Grooming",
    duration_minutes=40,
    priority=Priority.LOW,
    category="grooming",
    time="09:30",
))

# --- Whiskers's tasks ---
whiskers_scheduler = Scheduler(owner=owner, pet=whiskers)

whiskers_scheduler.add_task(Task(
    name="Feeding",
    duration_minutes=10,
    priority=Priority.HIGH,
    category="nutrition",
    time="08:00",
))
whiskers_scheduler.add_task(Task(
    name="Litter Box Cleaning",
    duration_minutes=10,
    priority=Priority.MEDIUM,
    category="hygiene",
    time="08:15",
))
whiskers_scheduler.add_task(Task(
    name="Playtime",
    duration_minutes=20,
    priority=Priority.MEDIUM,
    category="enrichment",
    time="09:00",
    notes="use feather wand",
))
whiskers_scheduler.add_task(Task(
    name="Brushing",
    duration_minutes=15,
    priority=Priority.LOW,
    category="grooming",
    time="09:30",
))

# --- Print plans ---
print("=" * 55)
print(biscuit_scheduler.explain())
print("=" * 55)
print(whiskers_scheduler.explain())
print("=" * 55)
