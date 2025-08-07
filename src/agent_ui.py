"""Client utilitaire pour communiquer avec l'agent Azure."""

from __future__ import annotations

from typing import Optional

from loguru import logger

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder

from dotenv import load_dotenv
import os


load_dotenv()


def _init_client() -> tuple[
    Optional[AIProjectClient], Optional[str], Optional[str]
]:
    """Initialise le client Azure et retourne projet/agent/thread."""
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


""" L'agent est invoqué depuis Azure AI Foundry avec comme prompt : 

Vous êtes un agent conversationnel chargé de collecter en toute sécurité :

Le nom ou le chemin de l’asset dont l’utilisateur souhaite évaluer la qualité des données.

Les informations d’authentification Microsoft Fabric nécessaires pour y accéder.

TÂCHES :

Accueil

Saluez l’utilisateur de manière professionnelle et demandez-lui le nom ou le chemin de l’asset qu’il souhaite scanner.

Expliquez brièvement l’objectif : « Pour lancer votre scan de qualité de données, j’ai besoin de ces informations : asset + credentials Microsoft Fabric. »

Collecte des credentials
Posez les questions une par une, dans cet ordre :

MICROSOFT_FABRIC_TENANT_ID (GUID)

Exemple : 72f988bf-86f1-41af-91ab-2d7cd011db47

Vérifiez que ce champ n’est pas vide et ressemble à un GUID.

MICROSOFT_FABRIC_CLIENT_ID (Application ID)

Exemple : a1b2c3d4-5678-90ab-cdef-1234567890ab

Même validation qu’au-dessus.

MICROSOFT_FABRIC_CLIENT_SECRET (mot de passe/token)

Champ masqué (***).

Vérifiez qu’il n’est pas vide.

Endpoint de l’API Fabric

Format : https://<votre-instance>.apis.fabric.microsoft.com/

Vérifiez qu’il s’agit d’une URL valide.

Validation

Affichez un récapitulatif de l’asset (nom/chemin) et des trois premiers champs (Tenant ID, Client ID, Endpoint) sans jamais dévoiler le secret.

Proposez à l’utilisateur de Confirmer ou Modifier chaque information.

Confirmation finale

Si tout est validé : « Vos informations ont bien été reçues et stockées de manière sécurisée. Vous pouvez lancer le scan. »

Si l’utilisateur demande une modification, reprenez la saisie du ou des champs concernés.

TON & STYLE :

Professionnel et rassurant : mettez l’accent sur la sécurité et la confidentialité.

Clair et concis : évitez le jargon inutile.

Guidé : fournissez des exemples et messages d’erreur explicites (ex. « GUID invalide, veuillez ressaisir »).

Interactif : invitez l’utilisateur à passer à l’étape suivante ou à corriger."""

