import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler, Priority

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

CATEGORY_ICONS = {
    "exercise":   "🚶",
    "nutrition":  "🍽️",
    "health":     "💊",
    "grooming":   "✂️",
    "hygiene":    "🧹",
    "enrichment": "🎮",
}

PRIORITY_BADGE = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}

# ── session state bootstrap ───────────────────────────────────────────────────
if "owner" not in st.session_state:
    st.session_state.owner = None
if "scheduler" not in st.session_state:
    st.session_state.scheduler = None

# ── 1. Owner setup ────────────────────────────────────────────────────────────
st.header("1. Owner Info")

with st.form("owner_form"):
    owner_name = st.text_input("Your name", value="Alex")
    available_minutes = st.number_input(
        "Available minutes today", min_value=10, max_value=480, value=120, step=10
    )
    day_start_hour = st.number_input(
        "Day start hour (24h)", min_value=0, max_value=23, value=8
    )
    if st.form_submit_button("Save Owner"):
        st.session_state.owner = Owner(
            name=owner_name,
            available_minutes=int(available_minutes),
            day_start_hour=int(day_start_hour),
        )
        st.session_state.scheduler = Scheduler(owner=st.session_state.owner)
        st.success(f"Owner '{owner_name}' saved.")

if st.session_state.owner is None:
    st.info("Fill in owner info above to get started.")
    st.stop()

owner: Owner = st.session_state.owner
scheduler: Scheduler = st.session_state.scheduler

# ── 2. Add a pet ──────────────────────────────────────────────────────────────
st.header("2. Add a Pet")

with st.form("pet_form"):
    pet_name  = st.text_input("Pet name", value="Biscuit")
    species   = st.selectbox("Species", ["dog", "cat", "bird", "rabbit", "other"])
    breed     = st.text_input("Breed", value="Golden Retriever")
    age_years = st.number_input("Age (years)", min_value=0.0, max_value=30.0, value=3.0, step=0.5)

    if st.form_submit_button("Add Pet"):
        new_pet = Pet(name=pet_name, species=species, breed=breed, age_years=float(age_years))
        owner.add_pet(new_pet)
        st.success(f"Pet '{pet_name}' added.")

if not owner.pets:
    st.info("Add at least one pet to continue.")
    st.stop()

pet_names = [p.name for p in owner.pets]
st.caption(f"Pets registered: {', '.join(pet_names)}")

# ── 3. Add a task ─────────────────────────────────────────────────────────────
st.header("3. Add a Task")

with st.form("task_form"):
    target_pet_name = st.selectbox("Add task to pet", pet_names)
    task_name       = st.text_input("Task name", value="Morning Walk")
    duration        = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=30)
    priority        = st.selectbox("Priority", ["HIGH", "MEDIUM", "LOW"])
    category        = st.selectbox(
        "Category",
        ["exercise", "nutrition", "health", "grooming", "hygiene", "enrichment", "other"],
        format_func=lambda c: f"{CATEGORY_ICONS.get(c, '📋')} {c}",
    )
    notes     = st.text_input("Notes (optional)", value="")
    task_time = st.text_input("Preferred start time (HH:MM)", value="08:00")

    if st.form_submit_button("Add Task"):
        target_pet = next(p for p in owner.pets if p.name == target_pet_name)
        new_task = Task(
            name=task_name,
            duration_minutes=int(duration),
            priority=Priority[priority],
            category=category,
            notes=notes,
            time=task_time,
        )
        scheduler.add_task(new_task, target_pet)
        st.success(f"Task '{task_name}' added to {target_pet_name}.")

# ── Summary metrics ───────────────────────────────────────────────────────────
all_tasks = scheduler._all_tasks()
total_pending_minutes = sum(t.duration_minutes for t in all_tasks if not t.completed)

col1, col2, col3 = st.columns(3)
col1.metric("Pets", len(owner.pets))
col2.metric("Tasks", len(all_tasks))
col3.metric("Total task time", f"{total_pending_minutes} min")

# ── Time usage progress bar ───────────────────────────────────────────────────
if all_tasks:
    used_fraction = min(total_pending_minutes / owner.available_minutes, 1.0)
    pct = int(used_fraction * 100)
    bar_color = "#e74c3c" if used_fraction >= 1.0 else "#f39c12" if used_fraction >= 0.75 else "#2ecc71"
    st.markdown(
        f"**Time budget:** {total_pending_minutes} / {owner.available_minutes} min used ({pct}%)"
    )
    st.markdown(
        f"""
        <div style="background:#e0e0e0;border-radius:8px;height:16px;width:100%;margin-bottom:8px">
          <div style="background:{bar_color};width:{pct}%;height:16px;border-radius:8px;
                      transition:width 0.4s ease"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Current task summary ──────────────────────────────────────────────────────
for pet in owner.pets:
    if pet.tasks:
        with st.expander(f"{pet.name}'s tasks ({len(pet.tasks)})"):
            for t in pet.tasks:
                icon = CATEGORY_ICONS.get(t.category, "📋")
                badge = PRIORITY_BADGE.get(t.priority.value.upper(), "")
                st.write(
                    f"{icon} **{t.name}** — {t.duration_minutes} min "
                    f"{badge} `{t.priority.value.upper()}` @ {t.time}"
                    + (f" | {t.notes}" if t.notes else "")
                )

# ── 4. Generate schedule ──────────────────────────────────────────────────────
st.header("4. Generate Schedule")

if st.button("Generate Schedule"):
    if not all_tasks:
        st.warning("No tasks added yet. Add some above.")
    else:
        if scheduler.is_overbooked():
            st.warning(
                f"⚠️ {total_pending_minutes} min of tasks but only {owner.available_minutes} min available "
                "— lowest-priority tasks will be skipped."
            )

        plan = scheduler.generate_plan()
        scheduled_minutes = sum(t.duration_minutes for _, t in plan)

        # ── Schedule metrics ──────────────────────────────────────────────────
        s1, s2, s3 = st.columns(3)
        s1.metric("Scheduled tasks", len(plan))
        s2.metric("Scheduled time", f"{scheduled_minutes} min")
        s3.metric("Time remaining", f"{owner.available_minutes - scheduled_minutes} min")

        conflicts = scheduler.conflicts(plan)
        for warning in conflicts:
            st.error(warning)

        st.subheader(f"Daily Plan — {owner.name}'s Pets")
        if plan:
            for slot, task in plan:
                icon = CATEGORY_ICONS.get(task.category, "📋")
                badge = PRIORITY_BADGE.get(task.priority.value.upper(), "")
                pet_label = next(
                    (p.name for p in owner.pets if task in p.tasks), "?"
                )
                st.markdown(
                    f"**{slot}** — [{pet_label}] {icon} {task.name} ({task.duration_minutes} min) "
                    f"{badge} `{task.priority.value.upper()}`"
                    + (f"\n> {task.notes}" if task.notes else "")
                )

        st.divider()
        st.text(scheduler.explain())
