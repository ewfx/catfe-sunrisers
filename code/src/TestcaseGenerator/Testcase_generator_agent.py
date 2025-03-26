from typing import AsyncGenerator, List, Sequence

from autogen_agentchat.agents import BaseChatAgent  
from autogen_agentchat.base import Response  
from autogen_agentchat.messages import AgentMessage, ChatMessage, TextMessage  
from autogen_core.base import CancellationToken  
from VertexAI.VertexAI_generator import generate

import asyncio
import json


class TestcaseGeneratorAgent(BaseChatAgent):
    def __init__(self, name: str):
        super().__init__(name, "A Testcase Generator agent to generate testcases.")

    @property
    def produced_message_types(self) -> List[type[ChatMessage]]:
        return [TextMessage]

    def convert_testcases_to_list(self, testcases: str) -> List:
        list_object = json.loads(testcases)
        with open("Artifacts/test_cases.json", "w") as f:
            json.dump(list_object, f, indent=4)
        return list_object

    def generate_testcases(self, context, data_extracted):
        sample_json = str(
            {
                "endpoint": "/endpoint",
                "method": "GET/POST/etc",
                "body": "JSON body that can be loaded using json.loads",
                "expectedOutput": "JSON body that can be loaded using json.loads",
            }
        )

        # final_query = f"""You are a software QA expert. Below is the context of an API that needs to be tested:
        # {context}
        # From this context, you need to:
        # 1. Identify the scenario being tested.
        # 2. Determine the expected response structure based on the API endpoints and their purpose.
        # 3. Generate all possible test cases, ensuring full coverage, including:
        # - Valid responses
        # - Missing or incorrect fields
        # - Edge cases and error scenarios

        # The test cases must be formatted as a JSON list, where each test case includes:
        # - The correct HTTP method for each endpoint.
        # - A valid or invalid request body where applicable.
        # - The expected output, which follows the API's response structure.
        # For example:
        # {sample_json}
        
        # Note:
        # Use the sample data attached to generate the test cases

        # Ensure:
        # - The JSON response is a list of objects that can be directly parsed using `json.load()`.
        # - Each test case is relevant to the API functionality.
        # - STRICTLY DO NOT RESPOND WITH ANYTHING ELSE! DO NOT RESPOND WITH ```json or ```.
        # """
        
        final_query = f"""You are a software QA expert. Below is the context of an API that needs to be tested:
        {context} with help of the attached data {data_extracted}
        
        From this context, You need to:
        1. Determine the expected response structure based on the API endpoints and their purpose.
        2. Generate 3 test cases for each route, ensuring full coverage (STRICTLY ONLY FROM THE DATA THAT IS ALREADY PROVIDED), including:
            - Valid responses
            - Missing or incorrect fields
            - Edge cases and error scenarios

        The test cases must be formatted as a JSON list, where each test case includes:
            - The correct HTTP method for each endpoint.
            - Include the correct endpoint to hit along with the base url.
            - A valid or invalid request body where applicable.
            - The expected output, which follows the API's response structure.
        For example:
        {sample_json}
        
        Note:
        Use the sample data attached to generate the test cases

        Ensure:
        - The JSON response is a list of objects that can be directly parsed using `json.load()`.
        - Each test case is relevant to the API functionality.
        - STRICTLY DO NOT RESPOND WITH ANYTHING ELSE! DO NOT RESPOND WITH ```json or ```.
        """
        testcases = generate(final_query)
        return Response(chat_message=TextMessage(content=testcases, source=self.name))

    async def on_messages(
        self, messages: Sequence[ChatMessage], cancellation_token: CancellationToken
    ) -> Response:
        # no_of_cases = await asyncio.get_event_loop().run_in_executor(None, input, "Enter number of testcases: ")
        # scenario = await asyncio.get_event_loop().run_in_executor(None, input, "Enter detailed scenario: ")
        # requirement = await asyncio.get_event_loop().run_in_executor(None, input, "Enter requirement: ")

        # write context - fetch from PR
        # with open('Artifacts/context.txt', 'a') as file:
        #     file.write("\n" + context)

        # read context
        with open("Artifacts/context.txt", "r") as file:
            context = file.read()

        sample_json = str(
            {
                "endpoint": "/full-endpoint-with-hostname",
                "method": "GET/POST/etc",
                "body": "JSON body",
                "expectedOutput": "JSON body",
            }
        )

        final_query = f"""You are a software QA expert. Below is the context of an API that needs to be tested:
        {context}
        From this context, you need to:
        1. Identify the scenario being tested.
        2. Determine the expected response structure based on the API endpoints and their purpose.
        3. Generate all possible test cases, ensuring full coverage, including:
        - Valid responses
        - Missing or incorrect fields
        - Edge cases and error scenarios

        The test cases must be formatted as a JSON list, where each test case includes:
        - The correct HTTP method for each endpoint.
        - A valid or invalid request body where applicable.
        - The expected output, which follows the API's response structure.
        For example:
        {sample_json}

        Ensure:
        - The JSON response is a list of objects that can be directly parsed using `json.load()`.
        - Each test case is relevant to the API functionality.
        - STRICTLY DO NOT RESPOND WITH ANYTHING ELSE! DO NOT RESPOND WITH ```json or ```.
        """
        testcases = generate(final_query)
        return Response(chat_message=TextMessage(content=testcases, source=self.name))

    async def on_reset(self, cancellation_token: CancellationToken) -> None:
        pass


async def run_testcase_generator_agent() -> None:
    # Create a vertexai agent.
    testcase_generator_agent = TestcaseGeneratorAgent("testcase_generator_agent")
    response = await testcase_generator_agent.on_messages([], CancellationToken())
    testcases = response.chat_message.content
    return testcase_generator_agent.convert_testcases_to_list(testcases)


# Use asyncio.run(run_vertexai_agent()) when running in a script.
# await run_vertexai_agent()
# asyncio.run(run_vertexai_agent())