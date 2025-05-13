import os
from dotenv import load_dotenv


class Config:
    def __init__(self):
        self.clear_env()
        load_dotenv()

        self.host = os.getenv("HOST", "localhost")
        self.port = os.getenv("PORT", "5432")
        self.user = os.getenv("USER", None)
        self.password = os.getenv("PASSWORD", None)
        self.name = os.getenv("NAME", "RodinDB")

        self.secret = os.getenv("SECRET_KEY", None)

        self.database_url = f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    @staticmethod
    def clear_env():
        os.environ.pop("HOST", None)
        os.environ.pop("PORT", None)
        os.environ.pop("USER", None)
        os.environ.pop("PASSWORD", None)
        os.environ.pop("NAME", None)

        os.environ.pop("SECRET_KEY", None)


config = Config()
