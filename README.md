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
# LLMs are stateless: They don't have any memory.

1. Every API call for the LLM is a brand new call for LLM.
2. That new call is a new call and ends simultaneously.
3. So LLM does not remember our previous call.
4. This is called Statelessness.
5. Then how do ChatGPT, Claude, remember our previous chats?
6. Truth is Model doesn't remember anything, they send the entire conversation to the model every single time we make an API call (for context). (We don't see it but the model gets all the history of chats for the context).
7. So how does the LLM knows which message corresponds to user and which is the reply of assistant ? ( for this we use the role thing , we also send the type role along with message). for us role is user and assitant's role is assistant so  it can distinguish.
#Context Window
1. Ai models cannot read unlimited texts at once.
2. Every model has a maximum size of text it can look at in one call(This is called Context Window).This is measured in Tokens.
3. So the issue is context length exceeds or silent cutting of older messages hence quality of response drops. It also becomes slower due to large text size, also more tokens are used so more cost.
