import uvicorn
from config import settings

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=settings.enable_reload,
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level,
        access_log=settings.enable_access_log,
    )
