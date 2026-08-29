# Fable Advisor

`fable-advisor` is a portable Agent Skill that lets Codex consult Claude Fable 5 as a high-effort advisor through your existing Claude Code subscription.

The main agent prepares the work, calls Fable once for judgment or critique, waits without imposing a timeout, and saves Fable's clean response directly to Markdown.

## Requirements

- Claude Code CLI
- A Claude subscription with Fable access

Authenticate Claude Code in the environment where the skill will run:

```bash
claude auth login
claude auth status
```

The skill requires `claude.ai` subscription authentication and does not use API-key authentication.

## Install for Codex

Clone this repository into your personal skills directory:

```powershell
git clone https://github.com/mattlgroff/fable-advisor "$HOME\.codex\skills\fable-advisor"
```

Restart Codex if the skill does not appear immediately, then invoke it with `$fable-advisor`.

## How output is saved

Claude CLI does not provide an output filename flag. The skill runs Claude in print mode with `--output-format text`, then uses the current shell's native redirection to save stdout directly to a task-specific Markdown file. Stderr is redirected to a separate log file.

The calling agent chooses the prompt, result, and log paths before launch, retains those paths while it waits, and reads the exact result path after Claude exits successfully. No wrapper script or Python runtime is involved.

The invocation uses Fable 5 at high effort, does not configure prompt caching or count tokens, does not fall back to another model, and does not impose a timeout. Every call receives a persistent Claude session ID so an interrupted consultation can be resumed only after user authorization.

## License

MIT
