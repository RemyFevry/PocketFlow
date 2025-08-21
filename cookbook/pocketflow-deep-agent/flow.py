from nodes import UserCliNode, TriageNode, ToolCall
from pocketflow import AsyncFlow,Flow
import asyncio
async def user_cli_flow():
    shared = {
        "answers": [],
        "previous_response_id": None,
        "tool_calls": [],
        "tool_memory": {}
    }

    user_node = UserCliNode()
    triage_node = TriageNode()
    tool_call_node = ToolCall()

    user_node >> triage_node
    tool_call_node >> triage_node
    triage_node >> tool_call_node
    tool_call_node - "user" >> user_node
    

    flow = AsyncFlow(start=user_node)
    await flow.run_async(shared)

    return shared

if __name__ == "__main__":
    asyncio.run(user_cli_flow())