from fastapi import FastAPI, Header, status, Request
from typing import Optional
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database"""
    print("Starting server... initializing database")
    await initdb()
    yield
    print("Server is stopping...")
app= FastAPI()



@app.get("/health")
def health_check():
    return{
        "status":"healthy"
    }