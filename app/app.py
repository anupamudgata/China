import streamlit as st
import requests
import json
import time
import markdown

# Set page configuration
st.set_page_config(page_title="DeepSeek R1 Chatbot", page_icon="💬", layout="wide")

# Custom CSS for better appearance
st.markdown("""
<style>
.main .block-container {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
}
.stTitle {
    font-size: 2.5rem;
    font-weight: 700;
    color: #1a1a1a;
    text-align: center;
    margin-bottom: 0.5rem;
}
.stSubheader {
    font-size: 1.2rem;
    color: #6c757d;
    text-align: center;
    margin-bottom: 2rem;
}
.chat-container {
    background: white;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    padding: 2rem;
    margin: 2rem 0;
}
.chat-message {
    max-width: 80%;
    margin: 1rem 0;
}
.chat-message.user {
    background: linear-gradient(135deg, #007bff, #0056b3);
}
.chat-message.bot {
    background: white;
    border: 1px solid #e9ecef;
}
.chat-message .avatar {
    background: #f8f9fa;
    border: 2px solid #e9ecef;
}
.chat-message .content {
    font-size: 1.1rem;
}
.stTextInput {
    margin-top: 2rem;
}
.stTextInput>div>div>input {
    font-size: 1.1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.sidebar .stButton>button {
    margin: 0.5rem 0;
    background: linear-gradient(135deg, #6c757d, #495057);
}
</style>
""", unsafe_allow_html=True)

# App title
st.title("DeepSeek R1 Chatbot")
st.subheader("Powered by Ollama")

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

if "current_conversation" not in st.session_state:
    st.session_state.current_conversation = "New Chat"

if "conversations" not in st.session_state:
    st.session_state.conversations = {"New Chat": []}

# Function to check if Ollama is running
def check_ollama_status():
    try:
        response = requests.get("http://localhost:11434/api/version", timeout=2)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

# Function to convert markdown to HTML
def convert_markdown_to_html(text):
    # Convert markdown to HTML
    html = markdown.markdown(
        text,
        extensions=['fenced_code', 'codehilite', 'tables']
    )
    return html

# Function to communicate with Ollama API
def query_ollama(prompt, model="deepseek", system_prompt="", temperature=0.7, max_tokens=2000):
    try:
        # Check if Ollama is running first
        if not check_ollama_status():
            st.error("Ollama is not running. Please start Ollama first.")
            return None
            
        # Prepare the request payload
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        
        # Add system prompt if provided
        if system_prompt:
            payload["system"] = system_prompt
            
        # Send the request to Ollama
        start_time = time.time()
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=60  # Increased timeout for longer responses
        )
        response.raise_for_status()
        end_time = time.time()
        
        # Calculate response time
        response_time = round(end_time - start_time, 2)
        
        return {
            "text": response.json()["response"],
            "response_time": response_time
        }
    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with Ollama: {str(e)}")
        return None

# Function to start a new conversation
def start_new_chat():
    # Save current conversation if it exists
    if st.session_state.messages:
        st.session_state.conversations[st.session_state.current_conversation] = st.session_state.messages.copy()
    
    # Create a new conversation
    new_chat_name = f"Chat {len(st.session_state.conversations) + 1}"
    st.session_state.conversations[new_chat_name] = []
    st.session_state.current_conversation = new_chat_name
    st.session_state.messages = []

# Function to load a conversation
def load_conversation(conversation_name):
    st.session_state.current_conversation = conversation_name
    st.session_state.messages = st.session_state.conversations[conversation_name].copy()

# Function to clear the current conversation
def clear_conversation():
    st.session_state.messages = []
    st.session_state.conversations[st.session_state.current_conversation] = []

# Sidebar for model selection and settings
with st.sidebar:
    st.header("Settings")
    
    # Model selection
    model = st.selectbox(
        "Select Model",
        ["deepseek", "llama3.2:3b"],
        index=0
    )
    
    # Advanced settings with expander
    with st.expander("Advanced Settings"):
        system_prompt = st.text_area(
            "System Prompt",
            value="You are a helpful AI assistant powered by the DeepSeek R1 model.",
            height=100
        )
        
        temperature = st.slider(
            "Temperature",
            min_value=0.1,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Higher values make output more random, lower values more deterministic"
        )
        
        max_tokens = st.slider(
            "Max Tokens",
            min_value=100,
            max_value=4000,
            value=2000,
            step=100,
            help="Maximum number of tokens in the response"
        )
    
    # Conversation management
    st.header("Conversations")
    
    # New chat button
    if st.button("New Chat"):
        start_new_chat()
        st.experimental_rerun()
    
    # Clear conversation button
    if st.button("Clear Current Chat"):
        clear_conversation()
        st.experimental_rerun()
    
    # List of existing conversations
    st.subheader("Saved Chats")
    for conv_name in st.session_state.conversations.keys():
        if st.button(conv_name, key=f"conv_{conv_name}"):
            load_conversation(conv_name)
            st.experimental_rerun()
    
    # About section
    st.markdown("### About")
    st.markdown("""
    This app uses your local Ollama installation to chat with DeepSeek R1 model.
    
    Make sure Ollama is running and the DeepSeek model is installed.
    
    To install the model, run:
    ```
    ollama pull deepseek
    ```
    """)
    
    # Status indicator
    ollama_status = check_ollama_status()
    status_color = "green" if ollama_status else "red"
    status_text = "Online" if ollama_status else "Offline"
    st.markdown(f"### Ollama Status: <span style='color:{status_color};'>{status_text}</span>", unsafe_allow_html=True)

# Display current conversation name
st.subheader(f"Current Chat: {st.session_state.current_conversation}")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            # Convert markdown to HTML for assistant messages
            st.markdown(message["content"], unsafe_allow_html=False)
        else:
            st.write(message["content"])

# Chat input
if prompt := st.chat_input("Ask something..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Display assistant response with a spinner
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response_data = query_ollama(
                prompt=prompt,
                model=model,
                system_prompt=system_prompt,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            if response_data:
                # Display the response with markdown support
                st.markdown(response_data["text"], unsafe_allow_html=False)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response_data["text"]})
                
                # Show response time
                st.caption(f"Response time: {response_data['response_time']} seconds")
                
                # Save current conversation
                st.session_state.conversations[st.session_state.current_conversation] = st.session_state.messages.copy()
            else:
                st.error("Failed to get a response from the model. Please check if Ollama is running.")
