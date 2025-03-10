# DeepSeek R1 Chatbot with Ollama and Streamlit

This is a simple web application built with Streamlit that allows you to chat with the DeepSeek R1 model using your local Ollama installation.

## Prerequisites

1. [Ollama](https://ollama.ai/) installed on your machine
2. DeepSeek R1 model pulled into Ollama
3. Python 3.7+ installed

## Setup Instructions

### 1. Install Ollama

If you haven't already installed Ollama, visit [ollama.ai](https://ollama.ai/) and follow the installation instructions for your operating system.

### 2. Pull the DeepSeek R1 model

Open a terminal and run:

```bash
ollama pull deepseek
```

This will download the DeepSeek R1 model to your local machine.

### 3. Install Python dependencies

Navigate to the project directory and install the required Python packages:

```bash
pip install -r requirements.txt
```

## Running the Application

1. Make sure Ollama is running in the background
2. Navigate to the project directory in your terminal
3. Run the Streamlit app:

```bash
cd app
streamlit run app.py
```

4. Open your web browser and go to http://localhost:8501

## Features

- Clean, user-friendly chat interface
- Model selection (DeepSeek or DeepSeek Coder)
- Chat history maintained during the session
- Error handling for Ollama connection issues

## Troubleshooting

- If you see an error about connecting to Ollama, make sure the Ollama service is running
- If the model is not responding, ensure you've successfully pulled the DeepSeek model using Ollama
- For any other issues, check the Streamlit and terminal logs for error messages

## Customization

You can modify the `app.py` file to change the UI, add more models, or customize the behavior of the chatbot.