from prompts.triage import TRIAGE as description
from tools import Tool
import asyncio
class Triage(Tool):
    name = "triage"
    in_post = dict(
        context={},
        metadata={"action","instructions"},
        chat={},
        memory={}
    )
    schema = {
            "type": "function",
            "name": "triage",
            "description": description,
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["web_search", "summarize", "stop", "user"],
                        "description": "The action to take, must be one of: web_search, summarize, stop, user",
                    },
                    "instructions": {
                        "type": "string",
                        "description": "Instructions for the action to take",
                    },
                },
                "required": ["action", "instructions"],
            },
        }

    async def exec(self):
        await asyncio.sleep(0)  # Simulate async operation
        return await super().exec()
