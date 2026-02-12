
from fastapi import FastAPI
from langserve import add_routes
from src.agents.general import general_agent

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple API server using LangChain's Runnable interfaces",
)

add_routes(
    app,
    general_agent,
    path="/general_agent",
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)