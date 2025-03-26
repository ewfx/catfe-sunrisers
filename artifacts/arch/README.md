# Context-Aware Testing System Architecture

This document outlines the architecture of a context-aware testing system designed to automatically detect changes in an application based on GitHub Pull Requests and generate and execute relevant test cases. The system leverages an Agentic AI-powered approach with several key components working in concert.

![image](https://github.com/user-attachments/assets/f5fce249-3f92-42ab-a239-eb08e6f17b79)

## Overview

The core idea is to monitor a GitHub repository for new Pull Requests. Upon detection, the system analyzes the changes introduced by the PR, understands the context of these changes in relation to the existing application and its testing context, generates new test cases accordingly, executes them against a sample application, and finally reports the execution results.

## Components

The system comprises the following key components:

1.  **Dummy App:** This represents the sample application that we want to test. It exposes APIs that can be called by the test cases.

2.  **GitHub Repo:** This is the repository hosting the application's codebase and potentially its data and testing context.

3.  **GitHub Webhooks:** This is the automation of event triggers within GitHub, that triggers the testing system upon creating a new Pull Request.

4.  **Agentic AI Powered Context Aware Testing System:** This is the central core of the testing system, housing the intelligent agents responsible for understanding, generating, and executing tests. It consists of the following sub-components:

    * **Context Extractor:**
        * **Trigger:** Activated by the Testcase generator.
        * **Functionality:**
            * Fetches the title and description of the Pull Request.
            * Reads the **Existing Context** (explained below).
            * Utilizes a Large Language Model (LLM) to summarize the information from the Pull Request and the existing context.
            * Updates the **Existing Context** with the summarized information, effectively incorporating the changes introduced by the PR into the system's understanding.

    * **Data Extractor:**
        * **Trigger:** Activated by the Testcase generator.
        * **Functionality:**
            * Monitors the data directory within the GitHub Repo for changes included in the Pull Request.
            * If changes are detected in the data directory, it extracts the latest mock data files.
            * This extracted mock data is then made available to the **Testcase Generator**.

    * **Testcase Generator:**
        * **Trigger:** Activated when a Pull Request is made on the app repo.
        * **Functionality:**
            * Reads the updated **Existing Context**.
            * Receives the extracted mock data from the **Data Extractor** (if any data changes were present).
            * Prompts an LLM with the contextual information (PR summary, existing context, and potentially new mock data) to generate relevant test cases.
            * Writes the generated test cases into the system (e.g., stores them in a temporary location or a dedicated test case management system).

    * **Testcase Executor:**
        * **Trigger:** Activated after the **Testcase Generator** has produced new test cases.
        * **Functionality:**
            * Reads the generated test cases.
            * Executes these test cases by making API calls to the **Dummy App**.
            * Captures the responses from the **Dummy App** for each executed test case.
            * Passes the execution status and captured responses to the **Testcase Execution Reporter**.

    * **Testcase Execution Reporter:**
        * **Trigger:** Activated after the **Testcase Executor** has finished running the test cases.
        * **Functionality:**
            * Receives the execution status and responses for all executed test cases.
            * Generates a comprehensive report of the test execution, typically in a PDF format.
            * This report would likely include details such as the test case description, execution status (pass/fail), and any captured responses or error messages.

5.  **Existing Context:** This represents the stored knowledge about the application's current state, functionality, and previous changes. It acts as the memory of the testing system. The **Context Extractor** reads and updates this context to ensure the system's understanding evolves with each Pull Request.

6.  **Reports:** These are the output of the **Testcase Execution Reporter**, providing a summary of the testing activities performed for a given Pull Request.

## Workflow

The typical workflow of the system is as follows:

1.  A developer creates a **Pull Request** in the **GitHub Repo** with changes to the application code or data.
2.  **GitHub Webhooks** are triggered by the new Pull Request.
3.  The triggered workflow initiates the **Agentic AI Powered Context Aware Testing System**.
4.  The **Context Extractor** fetches the PR details, reads the **Existing Context**, and uses an LLM to summarize the changes and update the **Existing Context**.
5.  The **Data Extractor** checks for changes in the data directory within the PR. If changes are found, it extracts the latest mock data.
6.  The **Testcase Generator** reads the updated **Existing Context** and the extracted data (if any) and prompts an LLM to generate relevant test cases based on the detected changes.
7.  The **Testcase Executor** reads the generated test cases and executes them by making API calls to the **Dummy App**, capturing the responses.
8.  The **Testcase Execution Reporter** receives the execution results and generates a detailed **Report**, likely in PDF format.

## Key Benefits

* **Automated Change Detection:** Automatically identifies changes introduced by Pull Requests.
* **Context-Aware Testing:** Generates test cases that are relevant to the specific changes and the overall application context.
* **Reduced Manual Effort:** Automates the process of test case generation and execution, reducing the manual effort required for testing.
* **Improved Test Coverage:** By understanding the context of changes, the system can potentially generate test cases that might be missed through manual testing.
* **Faster Feedback Loop:** Provides quicker feedback on the impact of code changes through automated testing.
* **AI-Powered Intelligence:** Leverages the capabilities of LLMs to understand code changes and generate intelligent test cases.

## Considerations

* **LLM Integration:** The effectiveness of the system heavily relies on the capabilities and prompt engineering of the LLMs used by the **Context Extractor** and **Testcase Generator**.
* **Existing Context Management:** Maintaining and evolving the **Existing Context** effectively is crucial for the system's accuracy and relevance over time.
* **Test Case Quality:** While AI-powered, the generated test cases might require review and refinement in certain scenarios.
* **Error Handling and Reporting:** Robust error handling and informative reporting mechanisms are essential for debugging and understanding test failures.
* **Integration with Dummy App:** The **Testcase Executor** needs to be properly configured to interact with the APIs of the **Dummy App**.

This architecture provides a foundation for building a sophisticated context-aware testing system that can significantly enhance the efficiency and effectiveness of software testing.
