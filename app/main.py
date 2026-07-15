from fastapi import FastAPI

from app.config import settings
from app.utils.logger import logger
from app.schemas.chat import ChatRequest, ChatResponse
from app.whatsapp.webhook import router as whatsapp_router
from app.services.scheduler import start_scheduler
from app.api.chat import router as chat_router
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import Base

logger.info("Starting Sentinel AI...")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://e-badawy.github.io",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(whatsapp_router)
app.include_router(chat_router)

@app.on_event("startup")
async def startup():

    logger.info("Application started successfully.")

    start_scheduler()


@app.get("/")
async def root():

    logger.info("Root endpoint called.")

    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "debug": settings.DEBUG,
    }
    
from app.agents.sentinel import agent

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):

    response = agent.chat(
        request.message
    )

    return ChatResponse(
        response=response
    )