from typing import AsyncGenerator, List, Sequence

from autogen_agentchat.agents import BaseChatAgent # type: ignore
from autogen_agentchat.base import Response # type: ignore
from autogen_agentchat.messages import AgentMessage, ChatMessage, TextMessage # type: ignore
from autogen_core.base import CancellationToken # type: ignore

import asyncio
import json
import os
import requests
import shutil
import stat
import subprocess
from dotenv import load_dotenv

load_dotenv()

class DataExtractorAgent(BaseChatAgent):
    def __init__(self, name: str):
        super().__init__(name, "A data extractor agent to send the data to be tested.")
        # GitHub repo details
        self.REPO_OWNER = os.getenv("REPO_OWNER")
        self.REPO_NAME = "sample-app"
        self.LOCAL_DIR = "./Artifacts/data"
        self.GITHUB_API_BASE = "https://api.github.com"

    @property
    def produced_message_types(self) -> List[type[ChatMessage]]:
        return [TextMessage]

    def remove_readonly(self, func, path, _):
        """Change the file permission and retry deletion."""
        os.chmod(path, stat.S_IWRITE)
        func(path)

    def safe_rmtree(self,directory):
        """Safely remove a directory, handling permission errors."""
        if os.path.exists(directory):
            shutil.rmtree(directory, onerror=self.remove_readonly)

    def get_pr_files(self,pr_number):
        """Fetch the list of changed files in the PR."""
        # url = f"{self.GITHUB_API_BASE}/repos/{self.REPO_OWNER}/{self.REPO_NAME}/pulls/{pr_number}/files"
        url = f"{self.GITHUB_API_BASE}/repos/dhiraj-inti/{self.REPO_NAME}/pulls/{pr_number}/files"
        response = requests.get(url)

        if response.status_code != 200:
            print("Error fetching PR files:", response.json())
            return []

        return [file["filename"] for file in response.json()]

    def update_data_dir(self, branch=None):
        """Pull the latest 'data' directory from the repo."""
        try: 
            repo_url = f"https://github.com/{self.REPO_OWNER}/{self.REPO_NAME}.git"

            
            # Clone the repository and fetch only 'data' directory
            subprocess.run(["git", "clone", "--depth", "1", "--filter=blob:none", "--sparse",  repo_url], check=True)
            subprocess.run(["git", "-C", self.REPO_NAME, "sparse-checkout", "set", "data"], check=True)
            subprocess.run(["git", "-C", self.REPO_NAME, "checkout"], check=True)
            # subprocess.run(["mv", f"{self.REPO_NAME}/data", "Artifacts/data"], check=True)
            if os.path.exists(self.LOCAL_DIR):
                self.safe_rmtree(self.LOCAL_DIR)
            shutil.move(f"{self.REPO_NAME}/data", "Artifacts")
            # subprocess.run(["rm", "-rf", self.REPO_NAME], check=True)  # Clean up
            if os.path.exists(self.REPO_NAME):
                self.safe_rmtree(self.REPO_NAME)
        except Exception as e:
            print(f"Error updating 'data' directory: {e}")

    def load_json_files(self):
        """Load JSON files from 'data' directory into a dictionary."""
        data_dict = {}

        if not os.path.exists(self.LOCAL_DIR):
            print(f"Directory '{self.LOCAL_DIR}' not found.")
            return data_dict

        for file_name in os.listdir(self.LOCAL_DIR):
            if file_name.endswith(".json"):
                file_path = os.path.join(self.LOCAL_DIR, file_name)
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        data_dict[file_name] = json.load(file)
                except Exception as e:
                    print(f"Error reading {file_name}: {e}")

        return data_dict

    async def on_messages(self, messages: Sequence[ChatMessage], cancellation_token: CancellationToken) -> Response:
        pass

    async def on_reset(self, cancellation_token: CancellationToken) -> None:
        pass


async def run_data_extractor_agent(pr_number, branch) -> None:
    data_extractor_agent = DataExtractorAgent("data_extractor_agent")
    changed_files = data_extractor_agent.get_pr_files(pr_number)
    print("CHANGED FILES================",changed_files)
    if any(file.startswith("data/") for file in changed_files) or not os.path.exists(data_extractor_agent.LOCAL_DIR):
        print("Changes detected in 'data/' directory. Updating local copy...")
        data_extractor_agent.update_data_dir(branch)
    else:
        print("No changes in 'data/' directory.")

    data_extracted = data_extractor_agent.load_json_files()
    return data_extracted

# print(asyncio.run(run_data_extractor_agent(2)))


# Use asyncio.run(run_data_extractor_agent()) when running in a script.
# await run_data_extractor_agent()

# asyncio.run(run_data_extractor_agent())
