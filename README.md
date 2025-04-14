# AI Task Automation Agent

This project implements an AI-powered agent that automates tasks on a local computer. The agent can be run through the command line or Terminal. The goal is to enable users to automate repetitive tasks by describing them in natural language, allowing the agent to generate a plan of actions using an AI API, get user approval, and execute the task locally. If the task fails, the agent refines the plan based on user feedback and retries the task.

## Project Overview

The AI Task Automation Agent is designed to:
1. Accept a task description in natural language.
2. Use a free AI API to generate a plan with the necessary commands or actions.
3. Display the generated plan to the user and request approval.
4. Execute the task once approved.
5. After execution, ask the user if the task was successful.
6. If the task fails, ask for the reason, refine the task using AI, and retry until successful.

### Example Task
- **Task**: "Generate a simple Python script to print 'Hello World' and execute it."
- The agent would generate the required code, execute it, and ensure it runs successfully.
- If there is a failure, the agent would fix the issue based on user feedback and re-run the task.

## Key Features

- Natural language processing to understand task descriptions.
- AI-driven task planning and command generation.
- Task execution on a local machine with file and command modifications.
- User approval before executing the task.
- Feedback loop for refining and retrying tasks in case of failure.

## Technologies Used

- **Python**: Programming language for implementing the agent.
- **AI API**: Used for generating task plans and handling task refinements.
- **Click**: Python library used to build the command-line interface (CLI).
- **OpenAI API or equivalent**: Used to process natural language inputs and generate executable plans (task generation).
