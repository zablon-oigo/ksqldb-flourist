from fastapi import FastAPI, Header, status, Request
from typing import Optional
from contextlib import asynccontextmanager
from  src.db.main import initdb

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database"""
    print("Starting server... initializing database")
    await initdb()
    yield
    print("Server is stopping...")


app= FastAPI(
    lifespan=lifespan
)


@app.get("/health")
def health_check():
    return{
        "status":"healthy"
    }