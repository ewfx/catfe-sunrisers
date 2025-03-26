from typing import AsyncGenerator, List, Sequence

from autogen_agentchat.agents import BaseChatAgent
from autogen_agentchat.base import Response 
from autogen_agentchat.messages import AgentMessage, ChatMessage, TextMessage
from autogen_core.base import CancellationToken
from VertexAI.VertexAI_generator import generate
import os
import asyncio
import json
import requests

class TestcaseExecutorAgent(BaseChatAgent):
    def __init__(self, name: str):
        super().__init__(name, "A Testcase Executor agent to execute testcases.")
        self.testcases = []
        self.BASE_URL = os.getenv("BASE_URL", "http://localhost:3000")

    @property
    def produced_message_types(self) -> List[type[ChatMessage]]:
        return [TextMessage]
    
    def read_testcases(self):
        with open('Artifacts/test_cases.json', 'r') as f:
            self.testcases = json.load(f)
            
    def check_output(self, tescase_output_array):
        
        prompt = f"""
        You are a software QA expert. Your task is to evaluate the results of API tests and determine the pass/fail status of each individual test case.

        You will receive a dictionary where:
            *Each key represents a URL that was tested.
            *Each value is a list representing the test cases executed against that URL. This list can contain:
            -> Individual strings: If only one test case was run for that URL, the value will be a two-element list [received_output, expected_output].
            -> Nested lists: If multiple test cases were run for that URL, the value will be a list of two-element lists, like this: [[received_output1, expected_output1], [received_output2, expected_output2], ...].

        For each test case (represented by a pair of received and expected outputs), compare the received_output with the expected_output. Consider contextual equivalence (e.g., "Divide by 0" and "Zero division error" are equivalent).

        Return a dictionary where:
            *Each key is a URL.
            *Each value indicates the test case status(es) for that URL:
            ->If the URL had only one test case, the value will be a single string: "PASS" or "FAIL".
            ->If the URL had multiple test cases, the value will be a list of strings (e.g., ["PASS", "FAIL", "PASS"]), with one "PASS" or "FAIL" for each test case executed against that URL.
        

        Note : Dont generate any code . The response generated must be a valid JSON so that it can be parsed using json.loads() function.
        STRICTLY DO NOT WRAP THE JSON USING ``` ```. 
        
        The input dictionary is as follows:
        {tescase_output_array}
        """
        
        output = generate(prompt)
        
        res = Response(chat_message=TextMessage(content=output, source=self.name))
        json_format = json.loads(res.chat_message.content)
        return json_format

    async def run_testcases(self):
        testcase_executions = []
        testcase_output_array = {}
        test_cases = self.testcases
        
        for test_case in test_cases:
            url = test_case['endpoint']
            method = test_case['method']
            body = json.loads(str(test_case['body']))  # Parse the JSON body
            expected_output = test_case['expectedOutput']
            try:
                print(self.BASE_URL + url)
                if method == 'POST':
                    response = requests.post(self.BASE_URL +  url, json=body)
                elif method == 'GET':
                    response = requests.get(self.BASE_URL + url )
            except Exception as e:
                print(e)
            # Add more methods as needed (e.g., PUT, DELETE)
            response_json = response.json()
            test_case["receivedOutput"] = json.dumps(response_json)

            if url in testcase_output_array:
                testcase_output_array[url].append([test_case["receivedOutput"], expected_output])
            else:
                testcase_output_array[url] = [[test_case["receivedOutput"], expected_output]]

            # if test_case["receivedOutput"] == expected_output:
            #     test_case["status"] = "PASS"
            # else:
            #     test_case["status"] = "FAIL"

            testcase_executions.append(test_case)
            
        test_results = self.check_output(testcase_output_array)
        
        for i in test_results:
            cnt=0
            for j in testcase_executions:
                if i == j['endpoint']:
                    if isinstance(test_results[i], list):
                        j['status'] = test_results[i][cnt]
                        cnt+=1
                    else:
                        j['status'] = test_results[i]

        return testcase_executions
            

    async def on_messages(self, messages: Sequence[ChatMessage], cancellation_token: CancellationToken) -> Response:
        pass

    async def on_reset(self, cancellation_token: CancellationToken) -> None:
        pass


async def run_testcase_executor_agent() -> None:

    testcase_executor_agent = TestcaseExecutorAgent("testcase_executor_agent")
    testcase_executor_agent.read_testcases()
    testcase_executions = await testcase_executor_agent.run_testcases()
    with open('Artifacts/test_cases_executed.json', 'w') as f:
        json.dump(testcase_executions, f, indent=4)


    


# Use asyncio.run(run_testcase_executor_agent()) when running in a script.
# await run_testcase_executor_agent()

#asyncio.run(run_testcase_executor_agent())