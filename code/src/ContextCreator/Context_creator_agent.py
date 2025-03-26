from typing import AsyncGenerator, List, Sequence

from autogen_agentchat.agents import BaseChatAgent  
from autogen_agentchat.base import Response  
from autogen_agentchat.messages import AgentMessage, ChatMessage, TextMessage  
from autogen_core.base import CancellationToken  
from VertexAI.VertexAI_generator import generate


import asyncio
import json
import requests


class ContextCreatorAgent(BaseChatAgent):
    def __init__(self, name: str):
        super().__init__(name, "A Context creator agent to consolidate and generate the context")

    @property
    def produced_message_types(self) -> List[type[ChatMessage]]:
        return [TextMessage]

    def generate_context(self, data):
        pre_context = ""
        with open("Artifacts/context.txt", "r") as file:
            pre_context = file.read()

        diff_url = data["pull_request"]["diff_url"]
        response = requests.get(diff_url)

        if response.status_code == 200:
            diff_content = response.text
        else:
            diff_content = ""

        query = f"""
        You are an expert in software documentation and contextual analysis. Your task is to refine and update the application's functional context, which will be used by an LLM agent for test case generation.

        Existing Context:{pre_context}

        New Code Changes:
        Title: {data["pull_request"]["title"]}
        Description: {data["pull_request"]["body"]}
        Code Diff: {diff_content}

        Task:
        Adding relevant details from the changes.
        Updating modified information.
        Removing outdated or redundant content.
        Keeping it precise, structured, and test-case relevant.
        
        Output:
        Provide the refined context in a clear, concise, and structured format.
        """
        context = generate(query)
        return Response(chat_message=TextMessage(content=context, source=self.name))

    async def on_messages(
        self, messages: Sequence[ChatMessage], cancellation_token: CancellationToken
    ) -> Response:

        data = await asyncio.get_event_loop().run_in_executor(None, input, "JSON payload: ")

        pre_context = ""
        with open("Artifacts/context.txt", "r") as file:
            pre_context = file.read()

        diff_url = data["pull_request"]["diff_url"]
        response = requests.get(diff_url)

        if response.status_code == 200:
            diff_content = response.text
        else:
            diff_content = ""

        query = f"""
        You are an expert in software documentation and contextual analysis. Your task is to refine and update the application's functional context, which will be used by an LLM agent for test case generation.

        Existing Context:{pre_context}

        New Code Changes:
        Title: {data["pull_request"]["title"]}
        Description: {data["pull_request"]["body"]}
        Code Diff: {diff_content}

        Task:
        Adding relevant details from the changes.
        Updating modified information.
        Removing outdated or redundant content.
        Keeping it precise and structured.

        Output:
        Provide the refined context in a clear, concise, and structured format.
        """
        context = generate(query)
        return Response(chat_message=TextMessage(content=context, source=self.name))

    async def on_reset(self, cancellation_token: CancellationToken) -> None:
        pass


async def run_context_creator_agent() -> None:
    # Create a vertexai agent.
    context_creator_agent = ContextCreatorAgent("context_creator_agent")
    response = await context_creator_agent.on_messages([], CancellationToken())
    context = response.chat_message.content
    return context


# Use asyncio.run(run_vertexai_agent()) when running in a script.
# await run_vertexai_agent()
# asyncio.run(run_vertexai_agent())
