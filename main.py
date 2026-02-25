
from fastapi import FastAPI
from langserve import add_routes
from src.api.resources.agent.server_chain import chain as agent_chain

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple API server using LangChain's Runnable interfaces",
)

add_routes(
    app,
    agent_chain,
    path="/agent",
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)