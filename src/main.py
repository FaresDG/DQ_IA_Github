from fastapi import FastAPI
from loguru import logger


app = FastAPI()


@app.get("/")
def read_root():
    """Basic root endpoint for the chatbot."""
    logger.info("Root endpoint called")
    return {"message": "Hello, World!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

    
