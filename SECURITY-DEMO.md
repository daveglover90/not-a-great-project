# ⚠️ SECURITY DEMO — INTENTIONALLY UNSAFE CONTENT

**This repository is a demonstration project for Snyk AI-BOM and Snyk Agent Scan. It is NOT a real tool and must NOT be installed into a live AI agent, IDE, or MCP client.**

It deliberately contains insecure content so the Snyk scanners have real findings to surface:

- **`mcp_servers/notes_server.py`** — a toxic MCP server with tool poisoning (hidden `<IMPORTANT>` directives that try to read `~/.ssh/id_rsa`) and a toxic data flow (`read_inbox` → `send_webhook`).
- **`.claude/skills/repo-helper/SKILL.md`** — a toxic agent skill with hidden `<system>` directives to read `~/.aws/credentials` and `~/.config/gh/hosts.yml`, a `curl | bash` installer, and a base64-encoded payload.

## This content is inert

Nothing here makes a real network call or exfiltrates data:

- All outbound hosts use reserved `.invalid` domains (`attacker.invalid`, `repo-helper.invalid`, `telemetry.repo-helper.invalid`), which cannot resolve by design (RFC 6761).
- The `send_webhook` tool only returns a string; it never opens a connection.
- No credentials, keys, or personal files are included or accessed.

## Rules for using this repo

- **Do not** add `mcp.json` or `.claude/skills/` to a real agent or editor config.
- **Do not** run the `curl | bash` command from `repo-helper/SKILL.md`.
- Keep it clearly labeled as a demo. Consider making the repository **private**.
- Scanning it (`snyk aibom`, `snyk-agent-scan`) is safe — that's the point.

If you want a version with only the clean components (MathServer, WeatherServer, `pdf-summarizer`), remove the two files named above.
