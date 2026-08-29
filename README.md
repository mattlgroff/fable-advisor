# Fable Advisor

`fable-advisor` is a portable Agent Skill for consulting Fable 5 as a high-effort advisor through Claude Code CLI.

It makes one explicitly authorized call, waits without imposing a timeout, saves stdout to Markdown, and returns the result to the calling agent.

## Requirements

- Claude Code CLI
- An authenticated Claude CLI credential with Fable 5 access

Authenticate Claude Code in the environment where the skill will run:

```bash
claude auth login
claude auth status
```

## Install for Codex

Clone this repository into your personal skills directory:

```sh
git clone https://github.com/mattlgroff/fable-advisor ~/.codex/skills/fable-advisor
```

Restart Codex if needed, then invoke `$fable-advisor`. The skill does not activate implicitly.

## How output is saved

Claude CLI has no response filename flag. The skill uses `--output-format text` and shell redirection to save stdout to a task-specific `.md` file. It uses no wrapper script or Python runtime.

## License

MIT
