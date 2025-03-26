# Context-aware Testing System Leveraging Generative AI

This is a versatile Python application that can be run in two modes:
1. **Menu-driven Mode**: A terminal-based interactive menu.
2. **Flask App**: A web application powered by Flask.

## Getting Started

Follow the steps below to set up and run the application:

```bash
# Clone the Repository
git clone <repository_url>
cd <repository_name>

# Create a Virtual Environment
python -m venv venv

# Activate the Virtual Environment
# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install Dependencies
pip install -r requirements.txt

# Create a .env File
# In the root directory, create a file named `.env` and add the following:
GOOGLEAI_STUDIO_API_KEY=YOUR_API_KEY
# Replace `YOUR_API_KEY` with your actual API key
REPO_OWNER=REPO_OWNER
# Replace REPO_OWNER with the github repo owner's ID
BASE_URL=BASE_URL_OF_YOUR_APP

# Running the Application

## Flask Web App:
python web_app_main.py
# Access the Flask app at: http://127.0.0.1:5000/
```


# 🚀 Context-aware Testing System Leveraging Generative AI

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)

---

## 🎯 Introduction
A Context-Aware Testing System enhances financial application testing by replacing static mock tools with an automated approach leveraging Generative AI. We aim to drastically improve efficiencies and ensure an application-agnostic, scalable solution for financial ecosystems. Our solution uses a multi-agent framework/Agentic AI that monitors GitHub for new pull requests, analyzes code changes, generates relevant test cases, executes them, and reports results. 

## 🎥 Demo
🔗 [Live Demo](#) (if applicable)  
📹 [Video Demo](#) (if applicable)  
🖼️ Screenshots:

![Screenshot 1](link-to-image)

## 💡 Inspiration
- Traditional testing is manual and lacks adaptability; AI-driven automation improves efficiency and reduces development cycles.
- Financial industry requires 300% more testing than others (Forrester Research, 2023).
- Financial services allocate 31% of IT budgets to QA/testing, the highest among industries (CapGemini Report 23-24).
- AI-powered testing boosts defect detection (up to 90%), accelerates innovation (75% orgs), and enhances quality (60% orgs).
- Leverage LLMs through an Agentic AI framework to maximize efficiency, enabling faster time-to-market for financial applications.


## ⚙️ What It Does
Replace-with-Architecture

## 🛠️ How We Built It
Replace-with-Architecture

## 🚧 Challenges We Faced
- **GitHub Workflow Integration:** Monitoring code changes and processing webhook events.
- **Dynamic Context Management:** Retrieving, updating context efficiently, tracking dependencies, and preventing outdated references.
- **LLM Prompt Optimization:** Engineering precise prompts to generate relevant, non-redundant test cases from PRs.
- **Edge Case Handling:** Mitigating flaky tests, ensuring mock data accuracy, and distinguishing real vs. expected failures.


## 🏃 How to Run
### ⚙️ Installation  

#### **1. Clone the Repository**  
```bash
git clone <repository_url>
cd <repository_name>
```  

#### **2. Create a Virtual Environment**  
```bash
python -m venv venv
```  

#### **3. Activate the Virtual Environment**  
- **Windows:**  
  ```bash
  .\venv\Scripts\activate
  ```  
- **Mac/Linux:**  
  ```bash
  source venv/bin/activate
  ```  

#### **4. Install Dependencies**  
```bash
pip install -r requirements.txt
```  



### 🔧 Configuration  

#### **1. Create a `.env` File**  
In the **root directory**, create a file named `.env` and add:  
```ini
GOOGLEAI_STUDIO_API_KEY=YOUR_API_KEY  # Replace with actual API key  
REPO_OWNER=REPO_OWNER  # Replace with GitHub repo owner's ID  
BASE_URL=BASE_URL_OF_YOUR_APP  # Replace with your app's base URL  
```  



### 🚀 Running the Application  

#### **Start Flask Web App**  
```bash
python web_app_main.py
```  
Access the app at: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)  



## 🏗️ Tech Stack
- **Programming Language:** Python
- **Backend:** Flask (for API and test execution management)
- **Agentic AI Framework:** Autogen (for context-aware test generation)
- **API Endpoint Management:** ngrok (for exposing local services securely)
- **LLM:** Gemini 1.5 Pro (for test case generation and context extraction)


## 👥 Team
- **Samarth Singh** - [GitHub](https://github.com/samarth1301) | [LinkedIn](https://www.linkedin.com/in/samarth-singh-a22247181/)
- **Dhiraj Inti** - [GitHub](https://github.com/dhiraj-inti) | [LinkedIn](https://www.linkedin.com/in/dhiraj-inti/)
- **Rahul Prasanth D** - [GitHub](https://github.com/rahulprasanth487) | [LinkedIn](https://www.linkedin.com/in/rahul-prasanth-d-7384ba1b9/)
- **Shria Sannuthi** - [GitHub](https://github.com/shriasannuthi) | [LinkedIn](https://www.linkedin.com/in/shria-sannuthi-4993ba208/)
- **Ravi Yogesh** - [GitHub](https://github.com/ravyogesh) | [LinkedIn](https://www.linkedin.com/in/raviyogesh/)
