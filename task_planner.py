import requests
import json
from typing import Dict, Any
from config import Config
import platform  


class TaskPlanner:
    def generate_plan(self, task_description: str) -> Dict[str, Any]:
        """Generate plan using local Ollama"""
        prompt = f"""
        [Task]: {task_description}
        
        Generate a JSON plan with:
        - "description": Brief summary
        - "commands": List of terminal commands (avoid chaining mkdir and cd with '&&'. Use 'mkdir -p <dir>' to avoid errors if the directory already exists)
        - "files": Files to create (with "path" and "content")
        - "warnings": Potential risks

        th
        Example:
        {{
            "description": "Create a Python hello world script",
            "commands": [
                "touch hello.py",
                "echo 'print(\"Hello World\")' > hello.py",
                "python3 hello.py"
            ],
            "files": [
                {{
                    "path": "hello.py",
                    "content": "print(\"Hello World\")"
                }}
            ],
            "warnings": "Overwrites hello.py if exists"
        }}
        """
        
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3",
                    "prompt": prompt,
                    "format": "json",
                    "stream": False
                }
            )
            response.raise_for_status()
            plan = json.loads(response.json()["response"])

            
            if platform.system() == "Darwin":
                for i, cmd in enumerate(plan.get("commands", [])):
                    if "google-chrome" in cmd:
                        path = cmd.split("google-chrome", 1)[1].strip()
                        plan["commands"][i] = f'open -a "Google Chrome" {path}'

            return plan
        except Exception as e:
            raise Exception(f"Ollama error: {str(e)}")
