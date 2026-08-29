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

Run `scripts/invoke_fable.py` from this skill directory. It uses the `claude` executable available in the current environment.

```text
python scripts/invoke_fable.py --prompt-file <prompt.md> --output <advisor-result.md>
```

The helper enforces these invariants:

- Claude print mode through `claude -p`
- model `claude-fable-5`
- effort `high`
- Claude subscription authentication through `claude.ai`, never an API key
- no fallback model
- persistent Claude session ID for recovery
- clean Markdown on stdout, redirected directly to the requested file
- stderr saved separately beside the Markdown result
- no child-process timeout

Do not wrap the invocation in a shorter timeout. A quiet process is still running. Continue polling until it exits or the user cancels. If it fails, report the saved session ID, Markdown path, and log path. Do not retry automatically.

For authentication diagnostics that do not invoke a model:

```text
python scripts/invoke_fable.py --auth-check-only
```

For interrupted consultations, obtain permission and then resume the recorded session:

```text
python scripts/invoke_fable.py --resume <session-id> --prompt-file <follow-up.md> --output <advisor-result.md>
```

## Use the result

Read the generated Markdown result, summarize Fable's judgment to the user, and apply it to the current task when requested. Preserve the result file as an auditable artifact and provide its path. Treat Fable's output as advice, not automatically authoritative truth.
