---
name: fable-advisor
description: Consults Fable 5 at high effort for a second opinion, critique, or strategic judgment. Use only when the user invokes $fable-advisor or explicitly asks to consult Fable.
---

# Fable Advisor

An explicit invocation or request to consult Fable authorizes one call. Never retry without new permission.

1. Run `claude auth status`. If it does not report an authenticated Claude CLI, ask the user to authenticate. Accept any authenticated credential type.
2. Prepare a self-contained prompt with the relevant material, question, and constraints. Request only Markdown in response.
3. Choose a `.md` result path. Using the current shell's syntax, pass the prompt through stdin and redirect stdout from:

```sh
claude -p --model claude-fable-5 --effort high --output-format text
```

4. Wait for Claude to exit without a process timeout. On failure, report the error and stop.
5. Read the result, apply it to the task, and provide its path.
