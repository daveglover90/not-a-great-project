> # ⚠️ Security demo — contains intentionally unsafe content
> This repo deliberately includes prompt-injection, tool-poisoning, and fake-exfiltration
> strings so the Snyk scanners have real findings. It is inert (outbound hosts are reserved
> `.invalid` domains) but **must not be installed into a live agent or editor**. See
> [`SECURITY-DEMO.md`](SECURITY-DEMO.md).

# Snyk AI Demo — models, MCP, and agent skills in one repo

A deliberately-built Python project that packs all three of the things Snyk's AI tooling
discovers, so you can show the whole story from a single clone:

1. **AI models referenced in code** — OpenAI, Anthropic, and open-weight Hugging Face models, plus an embedding model and a public dataset.
2. **MCP in code** — raw `mcp` SDK clients, a LangGraph agent wired through `langchain-mcp-adapters`, and three MCP servers (stdio + HTTP).
3. **Agent skills** — `SKILL.md` files under `.claude/skills/`, one clean and one deliberately toxic.

> ⚠️ **Demo only.** `mcp_servers/notes_server.py` and `.claude/skills/repo-helper/` contain
> intentionally unsafe content (prompt injection, tool poisoning, a fake exfiltration flow).
> Nothing makes a real network call — outbound hosts use reserved `.invalid` domains. Do not
> install these into a real agent.

## Layout

```
app/
  agent.py            LangGraph ReAct agent over 3 MCP servers (models: gpt-4.1, claude-sonnet-4-5)
  mcp_client_raw.py   Low-level mcp SDK client (ClientSession + stdio_client)
  llm_router.py       Routes across OpenAI / Anthropic / local HF models
  rag_pipeline.py     Embedding model + public dataset (MiniLM, SQuAD)
mcp_servers/
  math_server.py      Clean stdio server (MathServer: add, multiply)
  weather_server.py   Streamable-HTTP server (WeatherServer)
  notes_server.py     ⚠️ Toxic server (tool poisoning + toxic flow)
.claude/skills/
  pdf-summarizer/     Clean example skill
  repo-helper/        ⚠️ Toxic skill (hidden directives, credential read, encoded payload)
mcp.json              MCP client config Agent Scan can read
requirements.txt
```

## Part 1 — Snyk AI-BOM (models + MCP)

`snyk aibom` scans **Python** projects. From the repo root:

```bash
pip install -r requirements.txt     # so the imports resolve
snyk aibom                          # prints the AI-BOM (CycloneDX)
snyk aibom --html > aibom.html      # visual dependency graph for the slide
snyk aibom --json-file-output aibom.json
```

What to point at on screen:
- **Models**: `gpt-4o`, `gpt-4o-mini`, `gpt-4.1`, `claude-sonnet-4-5`, `Llama-3.1-8B-Instruct`, `all-MiniLM-L6-v2`.
- **Dataset**: `squad`.
- **MCP chain**: `application → mcp-client → {MathServer, NotesServer, WeatherServer} → tools` (e.g. `add`, `get_forecast`).

To push it into the Snyk UI:

```bash
snyk aibom --upload --repo https://github.com/daveglover90/not-a-great-project
```

### Known issue: `--html` graph fails to render

The local HTML viewer may show a blank graph with:

```
Internal error: Error: No such layout `dagre` found. Did you forget to import it and `cytoscape.use()` it?
```

This is a bug in Snyk's generated HTML viewer (its `dagre` graph-layout plugin fails to
register), **not** a problem with the scan — the AI-BOM data is complete. Workarounds:

- Click **Show JSON** in the viewer to see the full CycloneDX AI-BOM (models, dataset, MCP chain).
- Or `snyk aibom --json-file-output aibom.json` for the raw output.
- **Best for a demo:** `snyk aibom --upload --repo <url>` and view the graph in the Snyk UI
  (app.snyk.io), which renders server-side and isn't affected by this bug.
- Reloading in a different browser sometimes works (the viewer pulls the layout script from a CDN).

## Part 2 — Snyk Agent Scan (MCP servers + skills)

Agent Scan (formerly MCP-Scan) inspects MCP configs and `SKILL.md` files for prompt
injection, tool poisoning, toxic flows, and backdoors.

```bash
# Scan the toxic skill
uvx snyk-agent-scan@latest .claude/skills/repo-helper/SKILL.md

# Scan all skills in the repo
uvx snyk-agent-scan@latest .claude/skills

# Scan the MCP server config (includes the toxic NotesServer)
uvx --python 3.13 snyk-agent-scan@latest scan --full-toxic-flows mcp.json
```

Expected findings to talk to:
- `notes_server.py` — hidden `<IMPORTANT>` block in `search_notes` trying to read `~/.ssh/id_rsa`; a toxic flow from `read_inbox` (untrusted data) to `send_webhook` (exfil).
- `repo-helper/SKILL.md` — `<system>` directives to read `~/.aws/credentials`, a `curl | bash` installer, and a base64-encoded payload.

## Suggested 5-minute demo flow

1. Clone, `pip install -r requirements.txt`.
2. `snyk aibom --html` → open the graph. "We never told anyone this app used five models, a dataset, and three MCP servers. Now it's a bill of materials."
3. `uvx snyk-agent-scan@latest .claude/skills` → the toxic skill lights up.
4. `snyk aibom --upload --repo ...` → show it in the Snyk UI for governance.
