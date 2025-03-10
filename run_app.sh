#!/bin/bash

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/version > /dev/null; then
    echo "Error: Ollama is not running. Please start Ollama first."
    echo "You can start Ollama by running the 'ollama serve' command in a separate terminal."
    exit 1
fi

# Check if DeepSeek model is available
if ! curl -s http://localhost:11434/api/tags | grep -q "deepseek"; then
    echo "Warning: DeepSeek model might not be installed."
    echo "Would you like to pull the DeepSeek model now? (y/n)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo "Pulling DeepSeek model..."
        ollama pull deepseek
    else
        echo "Continuing without pulling the model. The app may not work correctly if the model is not available."
    fi
fi

# Install requirements if needed
if [ ! -f ".requirements_installed" ]; then
    echo "Installing Python requirements..."
    pip install -r requirements.txt
    touch ".requirements_installed"
fi

# Run the Streamlit app
echo "Starting DeepSeek R1 Chatbot..."
cd app
streamlit run app.py
