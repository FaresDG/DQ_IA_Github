"""Streamlit UI for asset selection (US1)."""

import streamlit as st
from loguru import logger


def main() -> None:
    """Render the Streamlit interface for asset selection."""
    st.title("Détection de la qualité des données")
    asset = st.text_input("Quel asset voulez-vous scanner ?")
    if st.button("Valider"):
        if not asset.strip():
            st.error(
                "Le champ ne peut pas être vide. Veuillez ressaisir.",
            )
            logger.warning("Asset path is empty")
        else:
            st.success(f"Asset sélectionné : {asset}")
            logger.info("Asset selected: %s", asset)


if __name__ == "__main__":
<<<<<<< HEAD
    main()
=======
    main()
>>>>>>> 14e1875e0cd9b7d21f561ef8ab1381919bd2f2a6
