import uvicorn

from api.app import create_app
from settings import settings

if __name__ == "__main__":
    app = create_app()
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=settings.PORT,
    )
