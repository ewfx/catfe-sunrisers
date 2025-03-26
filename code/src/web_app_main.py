from flask import Flask, render_template, request, jsonify, send_file
from TestcaseGenerator.Testcase_generator_agent import TestcaseGeneratorAgent
from ContextCreator.Context_creator_agent import ContextCreatorAgent
from TestcaseExecutor.Testcase_executor_agent import run_testcase_executor_agent
from TestcaseReportGenerator.Testcase_report_generator_agent import run_testcase_report_generator_agent
from DataExtractor.Data_extractor_agent import run_data_extractor_agent
from flask_cors import CORS
import time
import asyncio

app = Flask(__name__)
CORS(app)

@app.route('/contextualTesting', methods=['POST'])
def endpointHandler():
    data = request.get_json()  # Parses the JSON body
    startTesting(data)
    return jsonify({"message": "Contextual testing started"}), 200
def startTesting(data):
    # Step 1 - build context
    try:
        context = ''
        if data.get("action") == "opened":

            # read context + new context -> LLM(consider latest) -> summarized context -> write into context.txt
            context_creator_agent = ContextCreatorAgent("context_creator_agent")
            context = context_creator_agent.generate_context(data).chat_message.content

            # write context - fetch from PR
            with open("Artifacts/context.txt", "w", encoding="utf-8") as file:
                file.write(context)

        # Step 2 - Get the dummy data
        pr_number = data.get("number")
        data_extracted = asyncio.run(run_data_extractor_agent(pr_number))

        #Step 3 - Generate
        testcase_generator_agent = TestcaseGeneratorAgent("testcase_generator_agent")
        response = testcase_generator_agent.generate_testcases(context, data_extracted)
        testcases = testcase_generator_agent.convert_testcases_to_list(response.chat_message.content)
        
        #Step 4 - Execute
        asyncio.run(run_testcase_executor_agent())
    
        #Step 5 - Report the executions
        asyncio.run(run_testcase_report_generator_agent())
        return jsonify({"message": "Contextual testing started"}), 200
    except Exception as e:
        print(f"Error in startTesting: {e}")
        return jsonify({"message": "Error in startTesting"}), 500

if __name__ == '__main__':
    app.run(host="127.0.0.1",port=5000,debug=True)
