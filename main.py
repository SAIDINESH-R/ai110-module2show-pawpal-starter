from pawpal_system import Owner, Pet, Task, Scheduler, Priority

owner = Owner(name="Alex", available_minutes=120, day_start_hour=8)

biscuit = Pet(name="Biscuit", species="dog", breed="Golden Retriever", age_years=3.0)
whiskers = Pet(name="Whiskers", species="cat", breed="Siamese", age_years=5.0)

owner.add_pet(biscuit)
owner.add_pet(whiskers)

scheduler = Scheduler(owner=owner)

# --- Biscuit's tasks ---
scheduler.add_task(Task(
    name="Morning Walk",
    duration_minutes=30,
    priority=Priority.HIGH,
    category="exercise",
    time="08:00",
    notes="go to the park",
), biscuit)
scheduler.add_task(Task(
    name="Feeding",
    duration_minutes=10,
    priority=Priority.HIGH,
    category="nutrition",
    time="08:30",
), biscuit)
scheduler.add_task(Task(
    name="Flea Medicine",
    duration_minutes=5,
    priority=Priority.MEDIUM,
    category="health",
    time="09:00",
    notes="apply between shoulder blades",
), biscuit)
scheduler.add_task(Task(
    name="Grooming",
    duration_minutes=40,
    priority=Priority.LOW,
    category="grooming",
    time="09:30",
), biscuit)

# --- Whiskers's tasks ---
scheduler.add_task(Task(
    name="Feeding",
    duration_minutes=10,
    priority=Priority.HIGH,
    category="nutrition",
    time="08:00",
), whiskers)
scheduler.add_task(Task(
    name="Litter Box Cleaning",
    duration_minutes=10,
    priority=Priority.MEDIUM,
    category="hygiene",
    time="08:15",
), whiskers)
scheduler.add_task(Task(
    name="Playtime",
    duration_minutes=20,
    priority=Priority.MEDIUM,
    category="enrichment",
    time="09:00",
    notes="use feather wand",
), whiskers)
scheduler.add_task(Task(
    name="Brushing",
    duration_minutes=15,
    priority=Priority.LOW,
    category="grooming",
    time="09:30",
), whiskers)

# --- Print combined plan ---
print("=" * 55)
if scheduler.is_overbooked():
    total = sum(t.duration_minutes for t in scheduler._all_tasks() if not t.completed)
    print(
        f"WARNING: {total} min of tasks but only "
        f"{owner.available_minutes} min available — some will be skipped."
    )
plan = scheduler.generate_plan()
for warning in scheduler.conflicts(plan):
    print(warning)
print(scheduler.explain())
next_slot = scheduler.next_available_slot(plan)
print(f"Next available slot: {next_slot}")
print("=" * 55)

# ── Persistence demo ──────────────────────────────────────────────────────────
owner.save_to_json("pawpal_save.json")
print("\nSaved to pawpal_save.json")

loaded = Owner.load_from_json("pawpal_save.json")
print(f"Loaded owner: {loaded.name} ({loaded.available_minutes} min available)")
for pet in loaded.pets:
    task_names = ", ".join(t.name for t in pet.tasks)
    print(f"  {pet.name} ({pet.species}): {task_names}")
