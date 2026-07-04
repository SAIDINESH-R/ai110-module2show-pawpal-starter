# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

1. Add a pet (name, species, breed, age)
2. Add and manage care tasks for a pet (walks, feeding, meds, grooming)
3. Generate and view a daily care schedule sorted by priority


- What classes did you include, and what responsibilities did you assign to each?

- **Owner**: Holds the owner's name and time availability for the day
- **Pet**: Stores pet details and belongs to an Owner
- **Task**: Represents a single care activity with name, duration, priority, category, and notes
- **Scheduler**: The brain — takes an Owner and Pet, holds their tasks, and generates a daily plan
- **Priority**: An enum (HIGH, MEDIUM, LOW) used by Task to rank importance


**b. Design changes**

- Did your design change during implementation?

- **Duplicate task storage** — both `Pet.tasks` and `Scheduler.tasks` hold tasks, creating confusion about the single source of truth. Plan to remove `Scheduler.tasks` and always read from `Pet.tasks` instead.

- **Scheduler takes one Pet, but Owner has many** — the current design limits scheduling to one pet at a time. Will revisit this when implementing `generate_plan()`.

- **Missing methods** — `Pet` has no `remove_task()`, `Owner` has no `remove_pet()`, and `Task` has no `mark_completed()` method despite having a `completed` field. These will be added in Phase 2.


- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

 The scheduler considers task priority (HIGH/MEDIUM/LOW), preferred start time (HH:MM), task duration, and the owner's total available minutes for the day.


- How did you decide which constraints mattered most?

- Priority mattered most because a pet's health tasks (medicine, feeding) should always be scheduled before optional ones (grooming, playtime).


**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The scheduler only detects conflicts between tasks it has already scheduled using sequential slots, not between a task's preferred time and its assigned slot. This means two tasks with overlapping preferred times won't trigger a conflict warning if the greedy scheduler assigns them sequential slots. This tradeoff keeps the logic simple and avoids crashes, but it means the schedule may not always reflect the owner's preferred timing exactly.


---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI tools throughout the project for design brainstorming (generating the 
UML diagram), code generation (class skeletons and method implementations), 
debugging (fixing the time sort key and test failures), and documentation 
(docstrings and commit messages). The most helpful prompts were specific ones 
that referenced exact files and described the exact behavior needed.


**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

When AI generated the initial skeleton, it made Scheduler a dataclass instead 
of a regular class. I caught this during review and asked it to fix it because 
Scheduler has behavior and state management, not just data storage. I verified 
the fix by checking that __init__ was properly defined and all methods worked 
correctly when running main.py.


---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested 7 behaviors: task addition, task completion status, overbooked 
scheduling skipping LOW priority first, completed tasks being excluded from 
the plan, weekly tasks only appearing on the correct day, clock slots rolling 
over correctly across the hour boundary, and conflict detection identifying 
overlapping tasks. These tests were important because they cover the core 
scheduling logic and the most likely failure points.


**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am confident (4/5) that the scheduler works correctly for the tested 
behaviors. Edge cases I would test next include: scheduling across multiple 
pets simultaneously, tasks with invalid time formats, an owner with zero 
available minutes, and weekly tasks when repeat_day is not set (-1).


---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
The scheduling logic came together cleanly the greedy algorithm with 
priority sorting works reliably and the explain() output is readable and 
informative. The separation between pawpal_system.py (logic) and app.py 
(UI) made debugging much easier.


**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would redesign the Scheduler to handle multiple pets simultaneously 
instead of one at a time. I would also replace the string-based time 
field with Python's datetime.time type to avoid parsing issues and 
make validation easier.


**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

The most important thing I learned is that designing the system on paper 
(UML) before writing code saves a lot of time. It also showed me that AI 
is most useful when given specific, file-referenced prompts — vague prompts 
produce generic code that doesn't fit the actual system.