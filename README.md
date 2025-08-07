````markdown
# IA au service de la qualité des données (POC)

Ce projet a pour objectif de proposer une **solution modulaire** pour détecter les anomalies de qualité des données de manière rapide et intuitive, sans nécessiter la définition manuelle de règles métiers. Le moteur d’analyse repose sur un système multi-agents IA (Azure AI Foundry) et s’appuie sur un catalogue de données, un orchestrateur, un framework de tests, et un dashboard de restitution.


## Architecture du POC

```text
+-------------+    +-------------+    +-------------+    +--------------+
| Chatbot     | -> | Orchestrator| -> | AI Foundry  | -> | Great Expect.|
| (Streamlit) |    | (Airflow)   |    | (Azure)     |    | (Runner)     |
+-------------+    +-------------+    +-------------+    +--------------+
       |                                                           |
       v                                                           v
 +----------------+                                        +--------------+
 | Data Lakehouse |                                        | Power BI     |
 | (MS Fabric)    |                                        | Dashboard    |
 +----------------+                                        +--------------+
       |                                                           ^
       v                                                           |
 +----------------+                                             |
 | Data Catalog   | <-------------------------------------------+
 | (Data Hub)     |
 +----------------+
````

**Technologies clés**:

* Chatbot API : Python (FastAPI) + Streamlit UI
* Orchestration : Apache Airflow
* Catalogue de métadonnées : Data Hub (MCP)
* Moteur IA : Azure AI Foundry multi-agents
* Exécution règles : Great Expectations
* Reporting : Power BI (API REST)
* CI/CD & Infra : Docker, Terraform, azure-pipelines

## Fonctionnalités (Epics & User Stories)

### Epic 1 : Initialisation via le chatbot

* **US1** : Sélection de l’asset (nom/chemin)
* **US2** : Saisie des credentials 
* **US3** : Validation des informations saisies
* **US4** : Lancement du scan et réception d’un jobId

### Epic 2 : Orchestration & collecte des métadonnées

* **US5** : Réception du job par Airflow
* **US6** : Connexion à la source et récupération de l’asset
* **US7** : Scan schéma & profilage des données
* **US8** : Ingestion des métadonnées dans Data Hub

### Epic 3 : Génération & stockage des règles métiers

* **US9** : Récupération des métadonnées
* **US10** : Récupération de l’asset pour contexte
* **US11** : Génération automatique des expectations
* **US12** : Stockage et versioning des règles
* **US13** : Publication pour feedback utilisateur

### Epic 4 : Exécution des contrôles & restitution

* **US14** : Exécution des expectations (GE Runner)
* **US15** : Collecte des enregistrements non-conformes
* **US16** : Analyse et explication des anomalies
* **US17** : Stockage historique des anomalies
* **US18** : Publication dans Power BI
* **US19** : Synthèse & notification via le chatbot

### Epic 5 : Industrialisation, maintenance et gouvernance

* **US20** : Pipeline CI/CD (build, tests, Docker)
* **US21** : Déploiement IaC (Terraform)
* **US25** : Gestion centralisée des secrets

## Prérequis

* Python 3.9+
* Docker & Docker Compose
* Accès à un workspace Azure et Data Hub
* Compte Power BI avec permissions d’API

## Installation & Mise en route

> **🚧 En cours d’implémentation**


## Roadmap & Prochaines Étapes

1. **Phase de prototypage** : US1–US4 (Chatbot minimal + Orchestration)
2. **Phase IA & règles** : US5–US13 (Multi-agents + Great Expectations)
3. **Phase restitution** : US14–US19 (Power BI + Synthèse chatbot)
4. **Industrialisation** : CI/CD, monitoring, sécurité


```
