from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

# Use .env file or environment variables to replace the default values of Config
class Config(BaseSettings):
    app_name: str = "FastAPI"
    debug: bool = False

    # Database
    db_user: str = ""
    db_password: str = ""
    db_url: str = "sqlite:///./test.db"

    # SQLAlchemy
    sql_echo: str = ""


config = Config()
