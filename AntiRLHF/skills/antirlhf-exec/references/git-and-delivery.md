# Git operations and delivery

Follow the project's actual integration workflow and the user's instructions for the current task. Inspect the working tree and existing branch before changing files.

## Choose the authorized Git action

For ordinary feature development in repositories that require PRs:

1. Create a semantically named branch from the approved base.
2. Make the coherent implementation and maintain useful commits while developing.
3. Open a pull request for the result; use required checks and review where the project calls for them.
4. Squash Merge according to the project workflow and remove the completed branch.

If the user asks for **an uncommitted ZIP**, preserve the existing Git history, index, branch and working-tree changes. Make the requested edits, package the repository with `.git`, and deliver it without committing or merging. The user's explicit delivery request controls the action.

A repository can use a different branching or merge policy. Read its current instructions and apply them. Do not substitute a direct default-branch push merely because a PR route is inconvenient.

## Use Git identifiers when the operation needs them

`git status`, `git diff`, the current branch and the target PR normally tell you enough to perform a coherent change. An API that updates one Git object may require its SHA; use the object identifier returned by the relevant API call. After an operation succeeds, use its result and proceed.

Avoid repeatedly building inventories of SHAs and proof tables for routine edits. When an exact commit identity is material to a merge, rebase, conflict resolution or release, use it as needed. The objective is a correct Git operation and a usable result.

## Deliver what was requested

Include code, documents or ZIP artifacts in the form requested. Report implemented behavior, any consequential constraints and the meaningful checks that were actually run. If a tool is unavailable, say which part of the requested delivery it prevents and complete the remaining authorized work.

When the user asks to preserve existing uncommitted changes, verify that they remain present in the delivered working tree. Avoid bundling unnecessary build artifacts, caches or credentials into a distributable ZIP; retain repository history and source files.
