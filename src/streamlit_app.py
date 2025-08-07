"""Streamlit chat UI delegating credential validation to the agent."""

import streamlit as st
from loguru import logger

from agent_ui import send_message


def main() -> None:
    """Render a simple chat interface with the Azure agent."""
    st.title("Détection de la qualité des données")

    state = st.session_state
    if "messages" not in state:
        state.messages = []
        # Let the agent greet the user and explain the credential collection flow
        greeting = send_message("Bonjour")
        state.messages.append({"role": "assistant", "content": greeting})

    # Display chat history
    for msg in state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Votre message"):
        state.messages.append({"role": "user", "content": prompt})
        logger.info("User message: %s", prompt)
        with st.chat_message("user"):
            st.markdown(prompt)
        response = send_message(prompt)
        state.messages.append({"role": "assistant", "content": response})
        logger.info("Agent response: %s", response)
        with st.chat_message("assistant"):
            st.markdown(response)


if __name__ == "__main__":
    main()
