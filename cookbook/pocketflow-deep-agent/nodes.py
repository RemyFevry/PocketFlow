from pocketflow import AsyncNode,AsyncParallelBatchNode,Node
import asyncio
from tools.core import Tool
from tools.triage import Triage
from utils.functions import call_llm_async,call_llm,call_tool,async_call_tool

TOOLS_REGISTRY = {
    t.schema["name"]: t for t in Tool.__subclasses__()
}
class TriageNode(AsyncNode):
    async def prep_async(self, shared):
       
        
        return shared["answers"], shared.get("previous_response_id")
    async def exec_async(self, prep_res):
        messages, previous_response_id = prep_res
        breakpoint()
        response = await call_llm_async(messages,
                                         previous_response_id=previous_response_id,
                                         tools=[TOOLS_REGISTRY["triage"].schema],
                                         tool_choice="required",
                                         max_tool_calls =1
                                         )
       
        return response
    async def post_async(self, shared, prep_res, exec_res):
        response = exec_res
        
        shared["previous_response_id"] = response.id
        
        # Filter function calls only for tool execution
        function_calls = [item for item in response.output if item.type == "function_call"]
        


        # shared["answers"] = response.output
        shared["tool_calls"] = function_calls
        
    
        await asyncio.sleep(0)
       
        return "default"

class ToolCall(AsyncParallelBatchNode):
    async def prep_async(self, shared):
        # Prepare the tool calls from shared state
        # Don't add tool_calls to answers yet, as they're already added in TriageNode
        
        return [{
            "tool": TOOLS_REGISTRY.get(t.name),
            "tool_call": t,
            "memory": shared["tool_memory"]
        } for t in shared["tool_calls"]]

    async def exec_async(self, prep_res):
        
        
        return await async_call_tool(**prep_res)

    async def post_async(self, shared, prep_res, exec_res_list):
        shared["answers"] += exec_res_list
        for a in exec_res_list:
            triage = "default"
            if a["metadata"]["name"] == "triage":
                shared["action"] = a["metadata"]["action"]
                triage = a["metadata"]["action"]
            a.pop("metadata")
        return triage
            
class UserCliNode(Node):
    def prep(self, shared):
        # Prepare the user CLI data from shared state
        text = input("Enter your message: ")
        shared["answers"] += [
            {
                "role": "user",
                "content": text
            }
        ]
       
        return  shared.get("previous_response_id")


    def post(self, shared, prep_res, exec_res):
        previous_response_id = prep_res
        shared["previous_response_id"] = previous_response_id

        return "default"