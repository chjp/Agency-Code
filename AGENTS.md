# Repository Guidelines

## Project Structure & Module Organization
- `agency.py` bootstraps the planner/developer duo, loads `.env`, and is the entry point for the terminal demo.
- `agency_code_agent/` hosts the primary coding agent, prompt templates, and `tools/`; reuse helpers under `agents/` and `tools/`.
- `planner_agent/` mirrors the coder wiring for planning flows—keep configuration toggles aligned when moving features.
- `shared/` exposes adapters consumed by multiple agents, while `subagent_example/` illustrates how to extend the swarm.
- `tests/` provides pytest coverage across tools, planner logic, and integration paths; mirror its layout for new scenarios.

## Build, Test, and Development Commands
- `python3.13 -m venv .venv && source .venv/bin/activate` prepares the supported runtime.
- `python -m pip install -r requirements.txt` installs Agency Swarm plus test dependencies.
- `sudo python agency.py` launches the interactive CLI demo (sudo is required on macOS for filesystem access).
- `python run_tests.py` ensures dependencies exist and executes the full pytest suite with repository defaults.
- `pytest tests/test_tool_integration.py -k handoff` targets the planner→developer handoff flow when iterating.
- `pre-commit run --all-files` enforces Ruff formatting and import sorting before you push.

## Coding Style & Naming Conventions
- Use 4-space indentation, targeted type hints, and docstrings on public agent or tool factories.
- Keep files snake_case, classes PascalCase, and instruction templates within `agency_code_agent/`.
- Run `ruff check . --fix` and `ruff format .` to satisfy linting; expose new hooks via `create_*` factory functions.

## Testing Guidelines
- Tests use pytest with `pytest-asyncio`; async cases require `@pytest.mark.asyncio`.
- Name new suites `test_<area>.py`, reuse fixtures from `tests/conftest.py`, and cover both success and failure paths.
- Extend `tests/test_tool_integration.py` whenever agent orchestration changes to prevent regressions.

## Commit & Pull Request Guidelines
- Write imperative, concise commit titles (e.g., `Enable planner retries`) and group related edits.
- PRs should call out altered prompts or instructions, list verification commands, and link issues or task tickets.
- Attach relevant CLI logs or screenshots for UX changes so reviewers can validate behaviour.

## Security & Configuration Tips
- Store provider keys and model overrides in `.env`; `dotenv` autoloads them in `agency.py`.
- Document new configuration flags in `README.md` and update both agent factories when you add models or reasoning modes.
