# Fable Advisor

`fable-advisor` is a portable Agent Skill that lets Codex consult Claude Fable 5 as a high-effort advisor through your existing Claude Code subscription.

The main agent prepares the work, calls Fable once for judgment or critique, waits without imposing a timeout, and saves Fable's clean response directly to Markdown.

## Requirements

- Python 3.10 or newer
- Claude Code CLI
- A Claude subscription with Fable access
- On Windows, WSL with Claude Code installed and authenticated

Authenticate inside WSL:

```bash
claude auth login
claude auth status
```

The helper requires `claude.ai` subscription authentication and intentionally rejects API-key authentication.

## Install for Codex

Clone this repository into your personal skills directory:

```powershell
git clone https://github.com/mattlgroff/fable-advisor "$HOME\.codex\skills\fable-advisor"
```

Restart Codex if the skill does not appear immediately, then invoke it with `$fable-advisor`.

## Direct usage

Check authentication without invoking Fable:

```powershell
python scripts/invoke_fable.py --auth-check-only
```

Run a consultation:

```powershell
python scripts/invoke_fable.py `
  --prompt-file consultation.md `
  --output fable-response.md
```

On Windows, the helper uses the `Ubuntu` WSL distribution by default. Override it with `--distro` or `FABLE_ADVISOR_WSL_DISTRO`.

The invocation uses Fable 5 at high effort, does not configure prompt caching or count tokens, does not fall back to another model, and does not impose a timeout. Every call receives a persistent Claude session ID. The Markdown result, stderr log, and metadata are kept together.

## License

MIT
