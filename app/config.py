import os

os.system("which python")
from pathlib import Path
import tomli
from pydantic_settings import BaseSettings


def get_version_from_pyproject():
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    with pyproject_path.open("rb") as f:
        data = tomli.load(f)
    return data["tool"]["poetry"]["version"]


class Settings(BaseSettings):
    app_name: str = "n8n Workflow Runner"
    debug: bool = False
    version: str = get_version_from_pyproject()
    description: str = "n8n Workflow Runner"

    # server settings
    host: str = "127.0.0.1"
    port: int = 8000
    enable_reload: bool = True

    # logging settings
    log_level: str = "info"
    enable_access_log: bool = True

    # 데이터베이스 설정
    DATABASE_URL: str = "postgresql+asyncpg://username:password@localhost/dbname"

    # n8n 관련 설정
    n8n_base_url: str = "http://localhost:5678"

    # aws settings
    AWS_ACCESS_KEY_ID: str = "AWS_ACCESS_KEY_ID"
    AWS_SECRET_ACCESS_KEY: str = "AWS_SECRET_ACCESS_KEY"
    AWS_DEFAULT_REGION: str = "AWS_DEFAULT_REGION"

    # mlflow settings
    MLFLOW_TRACKING_URI: str = "https://example.com"
    MLFLOW_REGISTRY_URI: str = "https://example.com"

    # workflow 관련 설정
    github_id: str = ""
    github_token: str = ""
    github_nvidia_processor_url: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
