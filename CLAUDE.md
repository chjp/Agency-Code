# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Setup and Environment
```bash
python3.13 -m venv .venv && source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
# Fix LiteLLM bug after requirements install:
python -m pip install git+https://github.com/openai/openai-agents-python.git@main
```

### Running the Agency
```bash
sudo python agency.py                          # Launch interactive terminal demo (sudo required on macOS)
```

### Testing
```bash
python run_tests.py                            # Run full test suite with dependency installation
python run_tests.py test_bash_tool.py          # Run specific test file
pytest tests/test_tool_integration.py -k handoff # Run specific test pattern
```

### Linting and Formatting
```bash
ruff check . --fix                             # Lint with auto-fix
ruff format .                                  # Code formatting
pre-commit run --all-files                     # Run all pre-commit hooks
```

## Architecture

This is an **Agency Swarm** multi-agent system built on the OpenAI Agents SDK with LiteLLM for multi-provider model support.

### Core Agents
- **AgencyCodeAgent** (`agency_code_agent/`): Primary developer with 14 tools (Bash, Edit, Read, Git, etc.)
- **PlannerAgent** (`planner_agent/`): Strategic planning and task breakdown specialist
- **Communication**: Bidirectional handoffs using `SendMessageHandoff`

### Agent Factory Pattern
All agents use factory functions (`create_agency_code_agent()`, `create_planner_agent()`) to avoid singletons and enable clean testing. Model-specific instructions are selected and rendered dynamically.

### Tool System Architecture
- **BaseTool inheritance**: All tools in `tools/` extend Agency Swarm's `BaseTool` with Pydantic validation
- **Precondition enforcement**: Edit/Write tools require prior Read tool usage to prevent blind modifications
- **Atomic operations**: MultiEdit ensures all-or-nothing file modifications
- **Shared context**: Tools use Agency Swarm's context system for cross-tool state tracking

### Hook System
- **SystemReminderHook** (`shared/system_hooks.py`): Injects periodic reminders about instructions and TODO status
- **MessageFilterHook**: Handles message deduplication and reordering for Anthropic models
- **Thread-safe execution**: Global locks prevent tool execution conflicts

### Model Support
- **Multi-provider**: OpenAI (GPT-4, GPT-5), Anthropic (Claude), X.AI (Grok) via LiteLLM
- **Adaptive reasoning**: Different reasoning efforts and model-specific optimizations
- **Instructions**: Model-specific instruction files with dynamic placeholder rendering

## Key Directories

- `agency.py` - Main orchestration file and entry point for terminal demo
- `agency_code_agent/` - Primary developer agent with tools and instructions
- `planner_agent/` - Strategic planning agent (mirrors coder structure)
- `tools/` - 14 shared tool implementations (Bash, Edit, Read, Git, etc.)
- `shared/` - Common utilities, hooks, and agent helpers
- `subagent_example/` - Template for creating new agents
- `tests/` - Comprehensive pytest suite with tool and integration tests

## Development Notes

### Creating New Agents
Use `subagent_example/` as a template. Follow the factory pattern and ensure model-specific instruction files exist.

### Tool Development
- Extend `BaseTool` from Agency Swarm
- Add comprehensive Pydantic validation
- Include both success and failure test cases
- Follow thread-safety patterns from existing tools

### Testing Patterns
- Use pytest with `pytest-asyncio` for async cases
- Reuse fixtures from `tests/conftest.py`
- Test both success and failure paths
- Cover agent handoff flows in integration tests

### Configuration
- Environment variables loaded via `dotenv` in `agency.py`
- Model and provider settings configurable via `.env`
- Update both agent factories when adding new models or reasoning modes