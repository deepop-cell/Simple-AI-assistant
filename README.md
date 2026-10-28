

A lightweight, terminal-based AI chat assistant built with Python. This project features an interactive chat loop to communicate with local AI models using the OpenAI API format and Ollama, and demonstrates advanced agentic behaviors like **Tool Calling**.

## Features
- **Interactive Chat Loop:** Continuous terminal-based conversation until you decide to exit.
- **Local LLM Integration:** Powered by Ollama, allowing you to run models locally without incurring cloud API costs.
- **OpenAI API Standard:** Utilizes the official `openai` Python package, making it easily adaptable to cloud models if needed.
- **Secure Configuration:** Uses environment variables to securely manage API keys and base URLs.
- **Agentic Tool Calling:** The LLM can autonomously decide to run local Python functions (like checking the weather or calculating math) to answer complex queries.

## Prerequisites
Before you begin, ensure you have the following installed:
- Python 3.x
- Ollama (with at least one model downloaded, e.g., `ollama run qwen2.5:3b` or `llama3.2`)

---

## Core AI Concepts Implemented

### 1. Handling Statelessness
LLMs are naturally stateless—they don't have built-in memory. Every API call is a brand new request, and the model forgets the previous turn immediately. 
* **The Fix:** To give the illusion of memory (like ChatGPT or Claude), we send the entire conversation history back to the model on every single API call.
* **Role Management:** We use `"role": "user"` and `"role": "assistant"` in our message history array so the LLM knows which messages it wrote and which ones the user wrote.

### 2. Managing the Context Window
Models cannot read unlimited text at once. The maximum amount of text a model can process in one call is its **Context Window**, measured in tokens. If the conversation history gets too long, it causes API failures, slow responses, and higher costs.
* **Solutions for scaling:**
  * *Sliding Window:* Dropping the oldest messages when a limit is reached.
  * *Summarization:* Asking the LLM to summarize past context before it gets too long.
  * *RAG (Retrieval-Augmented Generation):* Storing history in a vector database and only pulling relevant past chats.

### 3. System Prompts (Personality)
To give the AI a specific personality or behavior rules (e.g., "Act like a technical expert" or "Always answer within 20 words"), we inject a message at the very beginning of the array with `"role": "system"`. This fundamentally guides how the model generates all future responses.

---

## Tool Calling Architecture

Instead of just chatting, this assistant acts as an **Agent**. It has access to a toolkit of Python functions. 

### The Tool Execution Cycle
When a user asks a complex question, the program follows this exact 5-step loop:

<img width="301" height="473" alt="image" src="https://github.com/user-attachments/assets/92a4f1d8-328f-4326-8d34-7da7ba567a7d" />


1. **Tool Definitions + Messages:** The user asks a question (e.g., *"What's the weather in Paris?"*). The system sends this query along with a JSON list of available tools to the LLM.
2. **Tool Calls:** The LLM realizes it needs external data and replies with a `tool_call` request (e.g., `get_weather("Kharagpur")`) instead of generating standard text.
3. **Execute Function Code:** The Python script intercepts this request, maps it to the local function, and executes the actual Python code to get the result (e.g., `{"temperature": 14}`).
4. **Results (Second Call):** The script appends the function's output to the message history and sends all prior messages + the new tool data back to the LLM.
5. **Final Response:** The LLM reads the tool's output and formats it into a natural, human-readable response (e.g., *"It's currently 14°C in Kharagpur."*).

### Available Tools
* **`get_current_time`**: Returns the live system date and time.
* **`get_city_weather(city)`**: Hits the `wttr.in` API to fetch real-time weather data.
* **`calculate(num1, num2, operation)`**: Safely performs exact math operations.

### Why give an LLM a Calculator?
LLMs are probabilistic text engines, not calculators. They guess the next word based on patterns. For large numbers, they often "hallucinate" the wrong answer because they view numbers as text tokens rather than mathematical values.

Turning the AI into a Desktop Assistant

Most basic AI scripts just hit public APIs and print text. I wanted to push this project further by giving the agent actual read/write access to my local machine, turning it into a proper desktop assistant. 

Instead of relying on external web services, I added tools that use Python's built-in system libraries:

* **Browser Automation (`open_website`):** The AI can now physically launch my OS's default web browser and navigate to URLs using the `webbrowser` module. If I type *"Open my GitHub profile"*, it parses the intent and opens the window for me.
* **System Health Monitor (`get_system_info`):** Using the `shutil` and `platform` libraries, the agent can inspect my local hardware. It reads my root drive, calculates raw bytes into Gigabytes, and returns my OS version and free storage space.

## Architecture Notes: Fixing the "One-Pass" Problem

While building this, I realized the current architecture has a major flaw: it only does a single pass. 

Right now, the execution flow is strictly linear: 
User Prompt -> LLM picks a tool -> Python runs the tool -> LLM generates the final response. 

But this completely breaks down for dependent, multi-step questions. For example, if I ask, *"What's the weather at my current location?"* The LLM correctly decides to call the `get_location` tool first. The backend returns "Kharagpur". But because the code is linear, the LLM is forced to reply immediately. It just says "You are in Kharagpur" and the chat loop resets. It never gets the chance to actually check the weather.

### The Fix: Adding an Inner Agent Loop
To solve this, my next step is upgrading the main script to use a chained tool-calling loop (a basic ReAct loop).

Instead of forcing an answer after one tool execution, I'll wrap the LLM call in an inner `while` loop. Once a tool returns data, the code will hand that context *back* to the LLM and let it decide:
1. **"I need more info"** -> It fires another tool (e.g., now that it knows I'm in Kharagpur, it calls `get_city_weather("Kharagpur")`).
2. **"I'm done"** -> It generates the final text response to the user and breaks the loop.

This is the exact logic gap between a simple API wrapper and an autonomous agent, and it's what I'm currently implementing.
**The Fix:** I wrapped the orchestration layer in an inner agent loop (a basic **ReAct** loop). Now, when a tool returns data, the code hands that context *back* to the LLM and lets it decide:
1. **"I need more info"** -> It fires another tool in the chain (e.g., calls `get_city_weather("Kharagpur")`).
2. **"I'm done"** -> It generates the final text response and breaks the loop.

### Safety & Error Handling (Self-Healing)
Running autonomous loops locally introduced some interesting engineering challenges that I had to solve:
- **The Infinite Loop of Death:** If the AI hallucinates or gets confused, it can get stuck calling the same tool forever. I implemented a `MAX_STEPS` limit using a Python `for-else` block. If the AI hits 5 steps without answering, it forces a safe fallback message and breaks the loop to prevent crashes.
- **Self-Healing Tool Crashes:** If a Python function fails (like an API timeout), it used to crash the whole app. Now, I wrap tool executions in `try-except` blocks. If a tool fails, the error is caught, converted to a string, and fed *back* to the LLM. The AI actually reads its own error and apologizes or tries another approach.

---

## Known Limitations & Future Scope

Building this revealed some of the current fundamental limits of autonomous agents, especially on local hardware. Here is what I plan to tackle next:

1. **The Loop Tax (Time & Tokens):** Every iteration of the ReAct loop forces the local model to re-read the entire chat history and all 7 JSON tool schemas. It's computationally heavy. *Future fix: Tool consolidation (e.g., combining IP fetching and weather checking into one single tool).*
2. **Cascading Failures:** If Tool 1 returns a hallucinated or slightly wrong answer, Tool 2 will use that bad data, ruining the whole chain. *Future fix: Implementing self-correction system prompts ("If data looks suspicious, stop and ask the user for clarification before proceeding").*
3. **Small Model Planning Struggles:** Lightweight local models (like 1B or 3B parameters) struggle to juggle 7+ tools and can sometimes call them in the wrong order. *Future fix: Forcing a "Plan-and-Solve" architecture where the model is required to output a `<thought>` block detailing its numbered plan before it is allowed to execute any tools.*
4. **Prompt Injection & Security Risks:** Because this agent has read/write access to my local system (e.g., opening browsers, reading system info), it is vulnerable to prompt injection. A malicious input could trick the LLM into ignoring its system prompt and executing unauthorized, destructive tools. *Future fix: Sandboxing the execution environment, implementing strict input sanitization, and adding an "approval-in-the-loop" step where the agent must ask for explicit Y/N permission before running any system-level commands.*

---

## Developer Tooling & Debug Mode

When building autonomous loops, relying on basic `print()` statements quickly pollutes the terminal and makes it impossible to see what the agent is actually doing under the hood. To solve this, I implemented a custom logging system.

### Environment-Based Debugging
Instead of deleting `print` statements after testing, I introduced a `DEBUG` environment variable toggle in the `.env` file. 
- **Production Mode (`DEBUG=False`):** The user sees a clean, simple chat interface.
- **Developer Mode (`DEBUG=True`):** The terminal reveals the exact mechanical steps the code takes, including the raw JSON payloads being sent to and from the tools.

### Terminal Styling (ANSI Escape Codes)
To make the CLI visually distinct, I implemented terminal colorization from scratch without relying on heavy third-party libraries like `colorama`. 
Using native **ANSI Escape Codes** (e.g., `\033[91m` for red), I separated the UI styling logic into a dedicated `Utilities/utilities.py` module. This ensures the main orchestration loop (`app.py`) and tool definitions (`tools.py`) remain strictly focused on logic, adhering to the principle of separation of concerns.
# Streaming LLM Assistant with Tool Calling

I was building a simple AI assistant and noticed the TTFT (Time To First Token) was way too high when waiting for the full JSON response to generate. To fix the lag, I rewrote the core to handle true streaming. 

The tricky part was handling function/tool calls while streaming. When the model decides to use a tool (like fetching the weather for two different cities at once), it stops streaming text and starts streaming the tool arguments in interleaved chunks. This repo handles mapping those chunks by their index, reconstructing the JSON strings, executing the tools, and sending the results back to the model for the final streamed answer.

## What it does
- **Instant terminal output**: Uses `stream=True` and `flush=True` to print tokens exactly as they arrive.
- **Parallel Tool Calling**: Safely parses the `delta.tool_calls` array, accumulates the fragmented arguments, and fires off multiple tools simultaneously.
- **OpenAI API Compatible**: Works with the official OpenAI API, or local endpoints like Ollama/vLLM (tested with Qwen).

## Setup

1. Make sure you have the `openai` and `python-dotenv` packages installed.
2. Create a `.env` file in the root directory:
```text
base_url=your_api_endpoint_here
api_key=your_api_key_here
MODEL=your_model_name
## Graceful Stream Interruption (Ctrl+C)

If the model starts generating a massive wall of text or you realize you made a typo in your prompt, you don't want to kill the entire Python script just to stop it. 

I added a `try-except KeyboardInterrupt` block around the streaming execution. Now, if you hit `Ctrl+C` while the assistant is streaming, it catches the interrupt, immediately stops printing tokens, clears any pending tool calls, and cleanly drops you right back into the chat loop so you can ask your next question. No ugly Python traceback errors, just a clean exit back to the input prompt.
```
### Vector Embeddings & Semantic Search (RAG)
* **Tokenization & Vector Mapping:** Breaks down input text into tokens and maps each token ID to a high-dimensional dense vector that captures its deep semantic meaning.
* **Mathematical Similarity Matching:** Calculates the semantic relationship between the user's query and stored knowledge by computing the dot product (or cosine similarity) between their respective vectors.
* **Retrieval-Augmented Generation (RAG):** Uses this vector math to perform lightning-fast context retrieval, fetching the most highly correlated documents from a vector database (e.g., PostgreSQL with `pgvector`) and injecting them directly into the LLM's prompt.
*  Basically whenever a query is generated , we find the most similar vector db (by dot product ) of that query , this thing is called semantic search(it searches for similar things not exact literal words) .





