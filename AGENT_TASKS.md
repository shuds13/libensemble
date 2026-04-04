## Agent tasks

Base branch for all agent work: develop.

For each task, create a new branch from develop.
Never branch from main.
Never commit directly to develop.

Commits may be made only on task branches in this fork.
Prefer a single final commit per task.
If work is incomplete, checkpoint commits are allowed.
Mark incomplete work clearly in the commit message.
Never add or modify git remotes.
Only start a task if it is not dependent on a previous task that has not yet been pulled into develop.

---

## Tasks

### Add this file

Status: Not started

Add this file AGENT_TASKS.md to the repo.

### Create smaller testsuite

Status: Not started

Create a consolidated testsuite. I dont want to remove existing tests right now, but
dont want to run them all each time. Even the simple tests take too long for agent
regular checks. Try to find a set of tests that have good coverage and copy them to
a quick tests folder.  run them and make sure work and if take too long dont do tests that run too long, replace or change them. Do not change what runs on CI. the quicktests suite is just for you the agent to use in your work.
