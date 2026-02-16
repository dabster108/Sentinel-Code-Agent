# sentinel_agent/main.py
import os
from google.adk.cli.fast_api import get_fast_api_app
from agent import root_agent  # Import your agent

# Create FastAPI app using google-adk helper
app = get_fast_api_app(
    agent=root_agent,
    # NOTE: do not pass 'agent_dir' if your google-adk version does not support it
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
