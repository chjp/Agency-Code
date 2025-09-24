from agency_swarm import Agent
import os
from tools import Read, Bash, LS, Grep, Edit, Write, TodoWrite
from shared.agent_utils import (
    render_instructions,
    create_model_settings,
    get_model_instance,
)
from shared.run_logging import SessionRunLogger
from shared.system_hooks import SessionLoggingHook

def create_subagent_example(
    model: str = "gpt-5",
    reasoning_effort: str = "low",
    session_logger: SessionRunLogger | None = None,
) -> Agent:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    instructions = render_instructions(current_dir + "/instructions.md", model)
    logging_hook = SessionLoggingHook(session_logger) if session_logger else None

    return Agent(
        name="SubagentExample",
        description="A template subagent that can be customized for specific domain tasks.",
        instructions=instructions,
        tools=[
            Read,
            Bash,
            LS,
            Grep,
            Edit,
            Write,
            TodoWrite,
        ],
        model=get_model_instance(model),
        model_settings=create_model_settings(model, reasoning_effort, "detailed"),
        hooks=logging_hook if logging_hook else None,
    )
