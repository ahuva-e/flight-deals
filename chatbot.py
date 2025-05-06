import streamlit as st
from openai import AzureOpenAI


def chat():
    # Initialize Azure OpenAI client
    client = AzureOpenAI(
        api_key=st.secrets.OPENAI_API_KEY,
        api_version="2024-02-15-preview",
        azure_endpoint=st.secrets.OPENAI_API_ENDPOINT
    )

    st.title("🌴 Holiday Destination Chatbot")

    # Initialize session state for chat messages
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are a friendly chatbot helping users choose a holiday destination."}
        ]

    # Display all past messages
    for message in st.session_state.messages[1:]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Always show prompt last
    prompt = st.chat_input("Ask me where to go on holiday!")

    # If user sends a prompt, process it AFTER rendering
    if prompt:
        # Save user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate assistant response
        try:
            stream = client.chat.completions.create(
                model="gpt-35-turbo-16k",
                messages=st.session_state.messages,
                stream=True,
            )

            with st.chat_message("assistant"):
                response = st.write_stream(stream)

            # Save assistant message
            st.session_state.messages.append({"role": "assistant", "content": response})

            # Force a rerun so the prompt stays at the bottom
            st.rerun()

        except Exception as e:
            st.error(f"Something went wrong: {e}")
