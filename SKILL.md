---
name: fable-advisor
description: Consult Claude Fable 5 through the user's Claude Code subscription for a high-effort second opinion, judgment, critique, or strategic review of important work.
---

# Fable Advisor

Use Fable as a scarce senior advisor while Codex remains responsible for the main task.

## Authorization

Invoking `$fable-advisor`, or explicitly asking to consult Fable, authorizes one Fable call for the current request. If this skill was selected implicitly, ask for permission immediately before running Claude. Never make another Fable call, retry a failed call, or resume an interrupted call without permission.

## Prepare the consultation

Create a self-contained Markdown prompt containing the material Fable needs, the decision or review question, applicable constraints, and the desired output. Preserve important nuance and evidence. Do not add token counting, cost estimation, prompt-caching setup, or an alternate model workflow.

End the prompt by asking Fable to return only its advisor report in Markdown. Save the prompt in a temporary or task-specific file. Do not include credentials or unrelated private material.

## Invoke Fable

Use the `claude` executable available in the current environment. Before the first consultation, run `claude auth status` and confirm it reports Claude subscription authentication through `claude.ai`. If it is logged out or using an API key, stop and ask the user to run `claude auth login` in that environment.

Before launching Claude, choose and retain three task-specific paths:

- the Markdown prompt file
- the Markdown result file
- the stderr log file

Generate and retain a UUID for the Claude session. Launch `claude` with the following arguments, using the current shell's native syntax:

```text
claude -p --model claude-fable-5 --effort high --session-id <uuid> --output-format text
```

Provide the prompt file as standard input. Redirect standard output directly to the chosen Markdown result file and standard error to the chosen log file. Claude CLI has no flag for naming the response file. `--output-format text` produces the response on standard output, so shell redirection is the saving mechanism.

The invocation must preserve these invariants:

- Claude print mode through `claude -p`
- model `claude-fable-5`
- effort `high`
- Claude subscription authentication through `claude.ai`, never an API key
- no fallback model
- persistent Claude session ID for recovery
- clean Markdown on stdout, redirected directly to the chosen result file
- stderr saved separately beside the Markdown result
- no process timeout

Do not wrap the invocation in a shorter timeout. A quiet process is still running. Continue polling until it exits or the user cancels. If it fails, report the saved session ID, Markdown path, and log path. Do not retry automatically.

For an interrupted consultation, obtain permission and then run Claude print mode with `--resume <session-id>`, the same model, effort, and text-output settings, a follow-up prompt on standard input, and newly chosen result and log files. Do not also pass `--session-id` when resuming.

Do not use `--debug-file` as the result path because it contains debug logs, not Fable's response. Do not use `--file`; that option downloads Claude file resources and does not save model output.

## Use the result

Read the generated Markdown result, summarize Fable's judgment to the user, and apply it to the current task when requested. Preserve the result file as an auditable artifact and provide its path. Treat Fable's output as advice, not automatically authoritative truth.
