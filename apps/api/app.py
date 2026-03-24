"""
FastAPI Application factory and setup.
Main entry point for the Language Learning Framework API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from config import settings
from api import vocabulary, study, audio, progress
from utils.logger import get_logger

logger = get_logger(__name__)


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.
    
    Returns:
        Configured FastAPI instance
    """
    app = FastAPI(
        title="Language Learning Framework API",
        description="Local-first API for interactive language learning with spaced repetition",
        version="1.0.0",
        docs_url="/api/docs",
        openapi_url="/api/openapi.json"
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Health check endpoint
    @app.get("/health", tags=["health"])
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "service": "Language Learning Framework API"}
    
    # Root endpoint with API info
    @app.get("/", tags=["info"])
    async def root():
        """API root with available resources."""
        return {
            "service": "Language Learning Framework API",
            "version": "1.0.0",
            "endpoints": {
                "vocabulary": "/api/vocabulary",
                "study": "/api/study",
                "audio": "/api/audio",
                "progress": "/api/progress",
                "docs": "/api/docs",
                "health": "/health"
            }
        }
    
    # Register route modules
    app.include_router(vocabulary.router)
    app.include_router(study.router)
    app.include_router(audio.router)
    app.include_router(progress.router)
    
    # Exception handling
    @app.exception_handler(404)
    async def not_found_handler(request, exc):
        return JSONResponse(
            status_code=404,
            content={"detail": "Endpoint not found", "path": str(request.url)}
        )
    
    logger.info(f"FastAPI application created. CORS origins: {settings.CORS_ORIGINS}")
    
    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting API server on {settings.API_HOST}:{settings.API_PORT}")
    
    uvicorn.run(
        app,
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )
