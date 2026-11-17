import requests
import streamlit as st

st.set_page_config(
    page_title="SecureDev AI",
    page_icon="🛡️",
    layout="centered"
)

st.title("SecureDev AI")
st.caption("Your AI assistant for secure software development")

if "messages" not in st.session_state:
    st.session_state.messages = []


if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


if prompt := st.chat_input("Ask a security question..."):
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/chat",
                    json={"question": prompt},
                    timeout=180
                )

                response.raise_for_status()
                answer = response.json()["answer"]

            except requests.exceptions.RequestException:
                answer = "Unable to connect to the backend server."

            except (KeyError, ValueError):
                answer = "Invalid response from the backend server."

        st.write(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

