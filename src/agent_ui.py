"""Client utilitaire pour communiquer avec l'agent Azure."""

from __future__ import annotations

from typing import Optional

from loguru import logger

try:  # Les dépendances Azure peuvent être absentes dans l'environnement local.
    from azure.ai.projects import AIProjectClient
    from azure.identity import DefaultAzureCredential
    from azure.ai.agents.models import ListSortOrder
except Exception as exc:  # pragma: no cover - fallback silencieux
    AIProjectClient = None  # type: ignore[assignment]
    DefaultAzureCredential = None  # type: ignore[assignment]
    ListSortOrder = None  # type: ignore[assignment]
    logger.warning("Azure SDK non disponible: %s", exc)

from dotenv import load_dotenv
import os


load_dotenv()


def _init_client() -> tuple[
    Optional[AIProjectClient], Optional[str], Optional[str]
]:
    """Initialise le client Azure et retourne projet/agent/thread."""
    if AIProjectClient is None:
        return None, None, None

    try:
        project = AIProjectClient(
            credential=DefaultAzureCredential(),
            endpoint=os.getenv("AIProjectClient_endpoint"),
        )
        agent = project.agents.get_agent(os.getenv("AgentManager_ID"))
        thread = project.agents.threads.create()
        logger.info("Thread créé, ID: %s", thread.id)
        return project, agent, thread
    except Exception as error:  # pragma: no cover - dépendances externes
        logger.error("Échec d'initialisation de l'agent: %s", error)
        return None, None, None


_project, _agent, _thread = _init_client()


def send_message(content: str) -> str:
    """Envoie un message à l'agent et renvoie sa réponse.

    Si l'agent n'est pas disponible, la fonction renvoie simplement le
    message fourni (mode écho) pour permettre les tests locaux.
    """

    if not _project or not _agent or not _thread:
        logger.warning("Agent Azure indisponible, mode écho activé")
        return f"Vous avez dit: {content}"

    project, agent, thread = _project, _agent, _thread

    project.agents.messages.create(
        thread_id=thread.id, role="user", content=content
    )
    run = project.agents.runs.create_and_process(
        thread_id=thread.id, agent_id=agent.id
    )

    if run.status == "failed":  # pragma: no cover - dépendances externes
        logger.error("Exécution échouée: %s", run.last_error)
        return f"Erreur: {run.last_error}"

    messages = project.agents.messages.list(
        thread_id=thread.id, order=ListSortOrder.ASCENDING
    )

    # On récupère la dernière réponse de l'assistant
    for message in reversed(list(messages)):
        if message.role == "assistant" and message.text_messages:
            return message.text_messages[-1].text.value

    return "Aucune réponse."


__all__ = ["send_message"]
