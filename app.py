import streamlit as st
from anthropic import Anthropic
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Anthropic client
anthropic = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def initialize_session_state():
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'poems' not in st.session_state:
        st.session_state.poems = []

def main():
    st.title("🎨 AI Poetry Companion")
    
    initialize_session_state()
    
    # Sidebar for different features
    mode = st.sidebar.selectbox(
        "Choose Mode",
        ["Poetry Generator", "Poetry Analysis", "Writing Assistant"]
    )
    
    if mode == "Poetry Generator":
        poetry_generator()
    elif mode == "Poetry Analysis":
        poetry_analysis()
    else:
        writing_assistant()

def poetry_generator():
    st.header("Poetry Generator")
    theme = st.text_input("Enter a theme or topic for your poem:")
    style = st.selectbox("Choose poetry style:", 
                        ["Haiku", "Sonnet", "Free Verse", "Limerick"])
    
    if st.button("Generate Poem"):
        prompt = f"Create a {style} about {theme}. Make it creative and meaningful."
        
        response = anthropic.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        st.markdown(f"### Generated Poem\n{response.content[0].text}")
        
        if st.button("Save Poem"):
            st.session_state.poems.append({
                "theme": theme,
                "style": style,
                "content": response.content[0].text
            })

def poetry_analysis():
    st.header("Poetry Analysis")
    poem = st.text_area("Enter a poem for analysis:")
    
    if st.button("Analyze"):
        prompt = """Analyze this poem considering:
        1. Literary devices used
        2. Themes and symbolism
        3. Emotional impact
        4. Structure and form
        Provide a detailed but concise analysis."""
        
        response = anthropic.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": f"{prompt}\n\nPoem:\n{poem}"
            }]
        )
        
        st.markdown(f"### Analysis\n{response.content[0].text}")

def writing_assistant():
    st.header("Writing Assistant")
    
    for message in st.session_state.chat_history:
        role = "🤖 Assistant" if message["role"] == "assistant" else "👤 You"
        st.write(f"{role}: {message['content']}")
    
    user_input = st.text_input("Ask for writing advice or suggestions:")
    
    if st.button("Send"):
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        response = anthropic.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": user_input
            }]
        )
        
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response.content[0].text
        })
        st.rerun()

if __name__ == "__main__":
    main()

