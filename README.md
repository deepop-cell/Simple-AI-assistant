# Simple AI Assistant

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
