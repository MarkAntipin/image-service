import uvicorn

from api.app import create_app
from settings import get_settings

if __name__ == "__main__":
    settings = get_settings()
    app = create_app()
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=settings.PORT,
    )
