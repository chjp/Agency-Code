# 👨‍💻 Agency Code

Fully open sourced version of Claude Code built with [Agency Swarm](https://agency-swarm.ai/welcome/overview) framework.
## chjp new idea
That’s a solid approach. If you want a Claude-Code-style agent but much smaller, here are two high-signal bases to fork and shrink—plus a concrete “reduction plan” to get to a minimal Python repo.

Good bases to slim down
	•	Anthropic’s Claude Code — official agentic coding tool; shows planning, tool use, and repo-aware workflows. Heavier, but patterns map well to a coding agent.  ￼
	•	SST OpenCode — popular terminal-first coding agent with a clean split between UI and core; provider-agnostic. Start here if you like TUI patterns and want to study a mature loop, then port the core to Python.  ￼

(Other options are more IDE-extension oriented, e.g. kodu-ai/claude-coder, or researchy (OpenBMB RepoAgent/XAgent), but they’re less ideal for a tiny repo starting point.)  ￼

⸻

“Shrink-to-core” plan (works for Claude Code or OpenCode)

Goal: end with a ~400–800-line Python agent repo implementing:
plan → choose tool → act → observe → reflect → stop/continue, plus 4 tools (read/write file, ripgrep/code search, run tests, run shell).

Step 0 — Fork & inventory
	•	Fork the repo and identify only the modules that:
	1.	build prompts/plans, 2) decide actions/tool calls, 3) execute tools, 4) stream observations back.
	•	Ignore: TUI/VSCode UI, analytics/telemetry, auth providers you won’t use, multi-session orchestration, SDK clients.

Step 1 — Freeze the model adapter
	•	Keep just one model adapter (Claude or OpenAI). Hard-code to start; add env vars later.
	•	Extract the fewest prompt templates needed (task brief, repo context, tool schema, reflection).

Step 2 — Define tools as plain JSON

Implement 4 tools in Python with strict I/O:
	•	read_file(path), write_file(path, content, create_ok)
	•	search_code(query, globs, max_hits) (wrap ripgrep/ast-grep)
	•	run_tests(cmd) (captures exit code/stdout/stderr)
	•	shell(cmd) (with allowlist + timeout)

Step 3 — Build the loop

State machine with guardrails:

PLAN → ACT(tool_name, args) → OBSERVE(result) → REFLECT(decide next step or DONE)

	•	Enforce max tool calls per run (e.g., 12).
	•	Auto-retry once on tool error with the error text fed back into the prompt.
	•	Stop conditions: tests pass, or user-defined success string, or max steps.

Step 4 — Minimal repo structure

mini-code-agent/
  agent.py        # loop + planner + reflection (single file is fine)
  tools.py        # the 4 tools above (or inline in agent.py)
  prompts.py      # prompt snippets + system instructions
  sandbox/        # working dir (gitignored)
  tasks/          # sample tasks + tests (toy project)
  README.md       # usage + safety notes

Step 5 — Safety & DX
	•	Run all actions in sandbox/. Denylist paths like ~, /etc, .ssh, .git/.
	•	Timeouts on all shell commands; truncate long outputs before sending back to the model.
	•	Add a --dry-run flag that prints planned tool calls without executing.
	•	Unit tests: fake model that returns canned plans → verify the loop and tool serialization.

Step 6 — Nice-to-have (later)
	•	Repo map (file tree + LOC + top identifiers) given to the model as context.
	•	Diff review step: after write, show unified diff to model for self-check before commit.
	•	Optional git tool (stage/commit/branch) behind a feature flag.

⸻

Why these bases?
	•	Claude Code: shows an “agentic coding” UX (terminal/IDE, repo context, git workflows) you can emulate before paring down. It’s actively maintained by Anthropic and used widely, with ongoing development around the planning loop.  ￼
	•	OpenCode: large but cleanly structured and provider-agnostic; the separation makes it easier to identify the action loop and tools you want to replicate in a tiny Python port.  ￼

⸻

If you want, I’ll do a pass for you

Say the word and I’ll:
	1.	pick one (Claude Code or OpenCode),
	2.	list the exact files you can ignore vs. keep for the core loop, and
	3.	output a Python starter repo plan mapping each kept concept to a minimal function.

(We can tailor for your environment—e.g., run with Claude via API/Bedrock vs. OpenAI.)
## 🔥 Key features

- **Developer Agent**: The primary developer agent with the same set of tools as Claude Code.
- **Planner Agent**: Planner agent that acts exactly as Claude Code's planning mode.
- **Full Control**: Full access to all 14 tools from Claude Code, agency structure and prompts.
- **Easy Subagent Creation**: Simple subagent creation process using Cursor or Claude Code itself.

👨‍💻 Additionally, you can experiment by adding other features from Agency Swarm framework, unsupported by Claude Code, like multi-level hybrid communication flows.

## 🚀 Quick start

1. Create and activate a virtual environment (Python 3.13), then install deps:

   ```
   python3.13 -m venv .venv
   source .venv/bin/activate
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

   > ⚠️ There is currently a bug in LiteLLM with Anthropic reasoning models.  
   > To fix this, after installing the requirements, run:
   >
   > ```
   > python -m pip install git+https://github.com/openai/openai-agents-python.git@main
   > ```

2. Try the agency (terminal demo):

   ```
   python agency.py
   ```

- Don't forget to run the command with sudo if you're on macOS.
- The agent won't be able to edit files outside of your current directory.

## 📈 Session logging

- Every terminal run of `agency.py` writes to `agentrunlog/timestamp.log`, capturing the start time and the JSONL file generated for that session.
- Detailed transcripts (LLM prompts/responses, planner↔coder handoffs, tool invocations and outputs) stream into `agentrunlog/session-YYYYMMDDTHHMMSS.jsonl`.
- Each JSONL line is a structured event with `timestamp`, `event`, `agent`, and a `data` payload—handy for debugging or replaying how the agents worked through a task.
- Logs accumulate per session; delete files in `agentrunlog/` if you need a clean slate before the next run.

## 🔐 Model & API configuration

- Supply provider keys (e.g. OPENAI_API_KEY, ANTHROPIC_API_KEY) via a local `.env`; `dotenv` loads them automatically.

### Using OpenRouter

1. Add `OPENROUTER_API_KEY=your_key` to `.env` (optional: `LITELLM_API_BASE=https://openrouter.ai/api/v1`).
2. Set the `model` in `agency.py` (or when creating an agent) to an OpenRouter slug, for example `openrouter/anthropic/claude-3-5-sonnet`.
3. Restart the demo; LiteLLM will route traffic through OpenRouter using that key.

## 🔧 Adding Subagents

- To add a subagent, simply prompt _Cursor_ or _Claude Code_ itself. For example:

  ```
  Ask me questions until you have enough context to create a QA tester subagent for my project
  ```

  After that it should create another folder in the root directory called `qa_tester_agent/` and modify the `agency.py` structure.

- Additionally, there is a template in the `subagent_example/` folder that you can use to create a new subagent yourself.

## 📝 Demo Tasks

### 🌌 Particle Galaxy Simulator

```
Create a full-screen interactive particle galaxy simulator using HTML5 Canvas and JavaScript. Include:
  - 2000 glowing particles that form a spiral galaxy shape
  - Particles should have different colors (blues, purples, pinks, whites) and sizes
  - Mouse movement creates gravitational pull that attracts/repels particles
  - Click to create a "supernova" explosion effect that pushes particles outward
  - Add trailing effects for particle movement
  - Include controls to adjust: particle count, rotation speed, color themes (nebula/aurora/cosmic)
  - Add background stars that twinkle
  - Display FPS counter and particle count
  - Make it responsive and add a glow/bloom effect to particles
  All in a single HTML file with inline CSS and JavaScript. Make it mesmerizing and cinematic.
```

### 🎨 Multiplayer Pixel Art Board

```
Create a shared pixel art canvas like r/place using Next.js and Socket.io:

- 50x50 grid where each player can color one pixel at a time
- 16 color palette at the bottom
- See other players' cursors moving in real-time with their names
- 5-second cooldown between placing pixels (show countdown on cursor)
- Minimap in corner showing full canvas
- Chat box for players to coordinate
- Download canvas as image button
- Show "Player X placed a pixel" notifications
- Persist canvas state in JSON file
- Mobile friendly with pinch to zoom

Simple and fun - just a shared canvas everyone can draw on together. Add rainbow gradient background.
```

### 📚 Agency Swarm PDF Chat App

```
Create a Streamlit PDF chat app using PyPDF2 and OpenAI API with Agency Swarm framework:
- File uploader accepting multiple PDFs
- Extract and display PDF text in expandable sections
- Chat interface where users ask questions about the PDFs
- Use agency-swarm to create an agent that can answer questions about the PDFs. (Reference below)
   - Use file_ids parameter in agency.get_response_sync method for allowing the agent to use the uploaded files.
- Create an endpoint for uploading files to openai. (Reference below)
   - Set purpose to "user_data".
   - Attach file in file_ids parameter of get_response method in agency-swarm. (Check reference.)
- OPENAI_API_KEY is provided in the ./.env file. Copy it to the .env file in the backend server folder.
- Export conversation as markdown
Include sample questions and nice chat UI with user/assistant message bubbles.

References:
- agency-swarm quick start: https://agency-swarm.ai/welcome/getting-started/from-scratch
- Openai API file upload reference: https://platform.openai.com/docs/api-reference/files/create

Before starting the task make sure to first use the WebSearch tool to read the references above.

**Important**: The agency-swarm integration must **actually** work. Do not use any placeholder messages and do not come back to me until it's fully tested and completed. Run the backend server and test the integration.
```

## Contributing

We'll be supporting and improving this repo in the future. Any contributions are welcome! Please feel free to submit a pull request.
