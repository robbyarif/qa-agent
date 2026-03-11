# Financial Assistant CLI Agent

This project is a Command Line Interface (CLI) application that acts as a "Financial Assistant". It uses an LLM with Function Calling to answer user questions about mocked exchange rates and stock prices. 

This project act as the Assignment 1 (Building Your First Question Answering Agent), part of the **CE8014 Agentic AI: Foundations and Development** course (Spring 2026, Department of Computer Science and Information Engineering, National Central University). It utilizes the OpenAI Python SDK and points it toward Gemini's OpenAI-compatible API endpoint.

## Features Implemented
- **Function Map**: Dynamic tool execution routing without `if-else` chains.
- **Parallel Tool Calls**: Agent can handle resolving multiple tool requests in a single turn.
- **Structured Outputs**: Tool schemas enforce `strict: True` and disallow additional properties.
- **Environment Security**: Uses `python-dotenv` to ensure API keys are not hardcoded.
- **Error Handling**: Graceful error recovery for mocked missing data (e.g. searching for `GOOG` returns an error message without crashing).

## Prerequisites
- Python 3.8+
- A Google Gemini API Key

## Setup Instructions

1. **Install Dependencies**
   Install the required Python packages from the `requirements.txt` file (it is recommended to use a virtual environment):
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Environment Variables**
   Copy the provided `.env.example` file and rename it to `.env`:
   ```bash
   cp .env.example .env
   ```
   Alternatively, on Windows, you can rename it in the file explorer or use:
   ```cmd
   copy .env.example .env
   ```
   Then, open the newly created `.env` file and replace `your_api_key_here` with your actual Gemini API key.

## Running the Agent

Start the CLI application by running the `main.py` script:
```bash
python main.py
```

You can then chat with the agent. Type `exit` or `quit` to terminate the session.

### Benchmark Test Cases
The system was designed to handle the following specific test queries:
- `"Who are you?"` (Persona test)
- `"What is the price of NVDA?"` (Single tool execution)
- `"Compare the stock prices of AAPL and TSLA."` (Parallel tool execution)
- `"My name is [Your Name]."` followed by `"What is my name?"` (Memory test)
- `"What is the price of GOOG?"` (Robustness and Error Handling test)
