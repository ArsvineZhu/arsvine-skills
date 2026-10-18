# Keeping an implementation on its real task

Use this guide when beginning repository work, resuming after compaction, inheriting an existing working tree, or deciding whether a side finding belongs to the request.

## Start from current project state

Read the user's requested behavior and explicit constraints, the repository's current instructions, and the code that currently owns the affected behavior. Inspect Git status before broad edits so existing uncommitted work is visible. Distinguish current source from historical documentation and agent-generated proposals. Keep user edits and unrelated files intact.

Use three pieces of working context when a task is long:

```text
Objective: Implement live configuration updates through the management API and CLI.
Decisions: The configuration service owns mutation; callers use one domain shape.
Current Work: The API path works. CLI still edits an outdated data structure.
              Migrate its write path, remove the old converter, and exercise CLI -> API.
```

This is task state for the agent. It can live in the current context, an existing handoff file, or a user-requested document. It need not become a new reporting requirement at every step.

## Decide which discoveries belong to this change

A side issue belongs to the task when it blocks the requested behavior, shares the root structural cause, breaks a contract affected by the change, or is explicitly added by the user. Repair it as part of the coherent change.

An unrelated defect in an old test fixture need not turn a parser feature into a repository-wide data cleanup. Leave a short note for the user if relevant, then finish the requested feature. If the supposedly unrelated defect appears on the actual user path, investigate it and repair the owning behavior.

### Example: protect login state without constantly mentioning it

**User constraint:** Keep the current login during repository maintenance.

**While working:** Inspect whether operations alter credentials, profile directories, tokens, browser sessions, or services that store them. Avoid deleting or replacing that state. This requirement remains active for relevant later commands.

**After an unrelated linter failure:** Fix the linter issue or return to the original work. No new login check or announcement is useful if the linter never touched authentication state.

**If a necessary command would reset credentials:** change the command or ask for specific authorization before that action. Here the constraint has an actual operational consequence.

The constraint has a lifetime and an affected resource. Keep it active within that lifetime, not as a theme of every later answer.

## Return from a detour

After a debugging branch, identify what was repaired, what part of the objective remains, and the next actual edit. Keep test logs and old guesses available in Git or existing artifacts if they matter to later work; don't let them replace task state.

When the entire requested behavior works and the relevant checks are done, deliver. A fresh idea for an unrelated cleanup can become a separate proposal if the user asks for further work.
