from application import app
from configuration.config import Config
import uvicorn
import asyncio


if __name__ == "__main__":
    uvicorn.run(app.create_app(), host=Config.HOST, port=Config.PORT)
