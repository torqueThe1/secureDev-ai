
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
