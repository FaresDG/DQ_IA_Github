"""Streamlit UI for asset selection and discussion with the agent."""

import streamlit as st
from loguru import logger

from agent_ui import send_message


def main() -> None:
    """Render the Streamlit interface for asset selection."""
    st.title("Détection de la qualité des données")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Quel asset voulez-vous scanner ?"):
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )
        logger.info("User message: %s", prompt)

        with st.chat_message("user"):
            st.markdown(prompt)

        response = send_message(prompt)
        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )
        logger.info("Agent response: %s", response)

        with st.chat_message("assistant"):
            st.markdown(response)


if __name__ == "__main__":
    main()
