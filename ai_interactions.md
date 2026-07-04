# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

I asked the agent to refactor the Scheduler class to work across multiple pets instead of a single pet. The agent was given access to `pawpal_system.py`, `main.py`, and `tests/test_pawpal.py` simultaneously.

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->


- Read `pawpal_system.py` and identified the single-pet limitation
- Removed the `pet` parameter from `Scheduler.__init__`
- Added `_all_tasks()` helper to flatten tasks across all owner's pets
- Updated `generate_plan()`, `explain()`, `conflicts()`, `tasks_by_category()`, and `is_overbooked()` to use `_all_tasks()`
- Rewrote `main.py` to use a single `Scheduler(owner=owner)` with tasks added per pet
- Updated all tests in `test_pawpal.py` to use the new API
- Ran `python main.py` and `pytest` to verify everything passed



**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

I verified that the output correctly showed tasks from both pets labeled with `[Biscuit]` and `[Whiskers]`. I also confirmed the overbooked warning appeared correctly when total task time exceeded available minutes.

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | Claude Code (agent mode) | Claude Code (chat mode) |
| **Prompt** | "Refactor Scheduler to work across all pets in the Owner. Remove the pet parameter and use _all_tasks() to flatten tasks across all owner.pets. Update all methods and tests." | "How should I update Scheduler to support multiple pets?" |
| **Response summary** | Directly edited all 3 files, ran tests, and verified output automatically | Explained the approach in text and suggested code snippets to copy manually |
| **What was useful** | Made all changes atomically across multiple files with no manual copy-paste | Good for understanding the concept before implementing |
| **Problems noticed** | Agent occasionally made assumptions about file names (used uml.mmd instead of uml_draft.mmd) | Required manually copying and pasting every suggestion into files |
| **Decision** | Used agent mode for implementation | Used chat mode for planning and understanding |

**Which approach did you use in your final implementation and why?**

<!-- Your conclusion -->

I used agent mode for implementation tasks and chat mode for planning and understanding. Agent mode was faster and more reliable for multi-file changes, while chat mode helped me understand what the agent was doing before accepting its edits.
