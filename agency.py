import os
from datetime import datetime

from shared.utils import silence_warnings_and_logs

silence_warnings_and_logs()

import litellm  # noqa: E402 - must import after warning suppression
from agency_swarm import Agency  # noqa: E402 - must import after warning suppression
from agency_swarm.tools import (
    SendMessageHandoff,  # noqa: E402 - must import after warning suppression
)
from dotenv import load_dotenv  # noqa: E402 - must import after warning suppression

from agency_code_agent.agency_code_agent import (  # noqa: E402 - must import after warning suppression
    create_agency_code_agent,
)
from planner_agent.planner_agent import (  # noqa: E402 - must import after warning suppression
    create_planner_agent,
)
from subagent_example.subagent_example import (  # noqa: E402 - must import after warning suppression
    create_subagent_example,
)
from shared.run_logging import SessionRunLogger, create_session_logger  # noqa: E402

load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
litellm.modify_params = True

# switch between models here
# model = "anthropic/claude-sonnet-4-20250514"
model = "openrouter/openai/gpt-oss-120b"

if model.startswith("openrouter/") and not os.getenv("LITELLM_API_BASE"):
    # Default to OpenRouter base when using an OpenRouter slug.
    os.environ.setdefault("LITELLM_API_BASE", "https://openrouter.ai/api/v1")

log_dir = os.path.join(current_dir, "agentrunlog")
log_file = os.path.join(log_dir, "timestamp.log")


def build_agency(model_name: str, session_logger: SessionRunLogger | None = None) -> Agency:
    planner = create_planner_agent(
        model=model_name, reasoning_effort="high", session_logger=session_logger
    )
    coder = create_agency_code_agent(
        model=model_name, reasoning_effort="high", session_logger=session_logger
    )
    subagent_example = create_subagent_example(
        model=model_name, reasoning_effort="high", session_logger=session_logger
    )

    return Agency(
        coder,
        planner,
        name="AgencyCode",
        communication_flows=[
            (coder, planner, SendMessageHandoff),
            (planner, coder, SendMessageHandoff),
            # (coder, subagent_example) # example for how to add a subagent
        ],
        shared_instructions="./project-overview.md",
    )


agency = build_agency(model)

if __name__ == "__main__":
    os.makedirs(log_dir, exist_ok=True)
    session_logger = create_session_logger(log_dir)

    with open(log_file, "a", encoding="utf-8") as log_handle:
        log_handle.write(
            f"{datetime.now().isoformat()}\tterminal_demo\t{session_logger.path()}\n"
        )

    agency = build_agency(model, session_logger=session_logger)
    session_logger.log("session_start", agent="Agency", model=model)
    try:
        agency.terminal_demo(show_reasoning=False if model.startswith("anthropic") else True)
    finally:
        session_logger.log("session_end", agent="Agency")
    # agency.visualize()
