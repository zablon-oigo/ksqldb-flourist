import time
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.errors import AccountNotVerified

logger = logging.getLogger("uvicorn.access")
logger.disabled = True


def register_middleware(app: FastAPI) -> None:

    @app.middleware("http")
    async def custom_logging(request: Request, call_next):
        start_time = time.time()
        try:
            response = await call_next(request)
        except AccountNotVerified:
            return JSONResponse(status_code=403, content={"detail": "Account not verified"})
        except Exception as exc:
            
            return JSONResponse(status_code=500, content={"detail": str(exc)})
        
        process_time = time.time() - start_time
        return response

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],     
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )