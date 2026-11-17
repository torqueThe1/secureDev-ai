
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


# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

        if message.get("sources"):
            with st.expander("Retrieved Sources"):
                for source in message["sources"]:
                    st.write(
                        f"{source['file']} — "
                        f"Chunk {source['chunk_index']}"
                    )

        if message.get("code_examples"):
            with st.expander("Original Code Examples"):
                for example in message["code_examples"]:
                    st.caption(
                        f"{example['file']} — "
                        f"Chunk {example['chunk_index']}"
                    )
                    st.code(example["code"], language="python")


# Knowledge source selection
source_options = {
    "All Sources": "all",
    "FastAPI": "fastapi_oauth2_jwt.md",
    "OWASP": "owasp_authentication.md"
}

selected_source = st.selectbox(
    "Knowledge Source",
    options=list(source_options.keys())
)


# Chat input
if prompt := st.chat_input("Ask a security question..."):
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        sources = []
        code_examples = []

        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/chat",
                    json={
                        "question": prompt,
                        "source": source_options[selected_source],
                        "history": [
                            {
                                "role": message["role"],
                                "content": message["content"]
                            }
                            for message in st.session_state.messages[:-1]
                        ]
                    },
                    timeout=180
                )

                response.raise_for_status()
                result = response.json()

                answer = result["answer"]
                sources = result.get("sources", [])
                code_examples = result.get("code_examples", [])

            except requests.exceptions.RequestException:
                answer = "Unable to connect to the backend server."

            except (KeyError, ValueError):
                answer = "Invalid response from the backend server."

        st.write(answer)

        if sources:
            with st.expander("Retrieved Sources"):
                for source in sources:
                    st.write(
                        f"{source['file']} — "
                        f"Chunk {source['chunk_index']}"
                    )

        if code_examples:
            with st.expander("Original Code Examples"):
                for example in code_examples:
                    st.caption(
                        f"{example['file']} — "
                        f"Chunk {example['chunk_index']}"
                    )
                    st.code(example["code"], language="python")

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources,
        "code_examples": code_examples
    })
