"""Main FastAPI application exposing scan endpoint."""

import os
from uuid import uuid4

import requests
from fastapi import FastAPI, HTTPException
from loguru import logger
from pydantic import BaseModel


app = FastAPI()


class ScanRequest(BaseModel):
    """Payload received when triggering a scan."""

    asset: str
    credentials: dict


def publish_event(event: dict) -> None:
    """Publish the scan event to the Airflow entrypoint.

    The target URL is read from the ``AIRFLOW_EVENT_URL`` environment variable.
    If the variable is not defined the event will simply be logged.

    Parameters
    ----------
    event:
        Dictionary containing ``asset``, ``credentials`` and ``jobId`` keys.

    Raises
    ------
    HTTPException
        Raised if the HTTP request to the Airflow service fails.
    """

    url = os.getenv("AIRFLOW_EVENT_URL")
    if not url:
        logger.warning("AIRFLOW_EVENT_URL not set; event not sent: %s", event)
        return

    try:
        response = requests.post(url, json=event, timeout=10)
        response.raise_for_status()
    except requests.RequestException as exc:  # pragma: no cover
        logger.error("Failed to publish event: %s", exc)
        raise HTTPException(
            status_code=502, detail="Failed to publish event"
        ) from exc


@app.get("/")
def read_root() -> dict:
    """Basic root endpoint for the chatbot."""

    logger.info("Root endpoint called")
    return {"message": "Hello, World!"}


@app.post("/scan")
def start_scan(payload: ScanRequest) -> dict:
    """Trigger a data scan job.

    A new ``jobId`` is generated and included in both the response and
    the event sent to Airflow.
    """

    job_id = str(uuid4())
    event = {
        "asset": payload.asset,
        "credentials": payload.credentials,
        "jobId": job_id,
    }

    publish_event(event)

    logger.info("Scan event created for %s with job %s", payload.asset, job_id)
    return {"jobId": job_id}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
