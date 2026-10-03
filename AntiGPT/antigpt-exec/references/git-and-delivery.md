# Git and Delivery

Use the project integration flow:

1. start non-trivial work on an up-to-date semantic branch;
2. make coherent commits during implementation;
3. open the pull request when the authorized change is ready for review;
4. run the verification required by the current project contract;
5. integrate with squash merge;
6. delete the feature branch after integration.

Do not use a direct default-branch push as a workaround for PR, permission, tooling, or CI problems.

Delivery reports should state the implemented behavior, material structural changes, verification actually run, and any real remaining blocker. Avoid a second evidence narrative that simply restates command output.
