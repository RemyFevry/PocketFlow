from tools.core import Tool
from openai import OpenAI,AsyncOpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()
client_async = AsyncOpenAI()
import asyncio

import json
import yaml
def standardize_message(messages:list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        {
            "role": message["role"],
            "content": message["content"],
       
        }
        for message in messages
    ]
def call_llm(input:list[dict],**kwargs ) -> str:

    response = client.responses.create(
        model="gpt-5-nano",
        input=input,
    
        **kwargs
    )
    return response

async def call_llm_async(input:list[dict],**kwargs ) -> str:

    response = await client_async.responses.create(
        model="gpt-5-nano",
        input=input,
        **kwargs
    )
    return response




def call_tool(tool,tool_call, memory, environnement="cli"):
    if not tool:
        raise ValueError(f"Unknown tool: {tool_call.name}")
    # breakpoint()
    result = tool(memory=memory, environnement=environnement, **json.loads(tool_call.arguments))
    return {
    "type": "function_call_output",
    "call_id": tool_call.call_id,
    "output": result.text,
    "metadata": result.metadata
    }

async def async_call_tool(tool:Tool, tool_call, memory:dict, environnement="cli"):
    if not tool:
        raise ValueError(f"Unknown tool: {tool_call.name}")
    # breakpoint()
    tool_instance = tool(memory=memory, environnement=environnement, **json.loads(tool_call.arguments))
    await tool_instance.execute()
    return {
        "type": "function_call_output",
        "call_id": tool_call.call_id,
        "output": tool_instance.text,
        "metadata": tool_instance.metadata,
        # "reasoning": tool_call.reasoning
    }