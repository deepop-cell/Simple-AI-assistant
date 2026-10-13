# Simple AI Assistant

A lightweight, terminal-based AI chat assistant built with Python. This project features an interactive chat loop to communicate with local AI models using the OpenAI API format and Ollama.

## Features
* **Interactive Chat Loop:** Continuous terminal-based conversation until you decide to exit.
* **Local LLM Integration:** Powered by Ollama, allowing you to run models locally without incurring cloud API costs.
* **OpenAI API Standard:** Utilizes the official openai Python package, making it easily adaptable to cloud models if needed.
* **Secure Configuration:** Uses environment variables to securely manage API keys and base URLs.

## Prerequisites
Before you begin, ensure you have the following installed:
* Python 3.x
* Ollama (with at least one model downloaded, e.g., ollama run qwen3:4b)

## Installation

1. Clone the repository:
git clone [https://github.com/YOUR-USERNAME/simple-ai-assistant.git](https://github.com/YOUR-USERNAME/simple-ai-assistant.git)
cd simple-ai-assistant

2. Set up a virtual environment:
python -m venv .venv

3. Activate the virtual environment:
- For Windows: .venv\Scripts\activate
- For Mac/Linux: source .venv/bin/activate

4. Install the required dependencies:
pip install openai python-dotenv

5. Configure your environment variables:
Create a file named .env in the root directory of the project and add the following configuration:
base_url="[http://127.0.0.1:11434/v1](http://127.0.0.1:11434/v1)"
api_key="ollama" 
model="qwen3:4b" 

## Usage

1. Ensure Ollama is running in the background.
2. Start the AI assistant:
python simple_ai_assitant.py
3. Type your messages into the terminal. To end the conversation, type exit, quit, bye, or goodbye.
