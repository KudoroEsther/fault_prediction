import os
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv


REPO_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(REPO_ROOT / ".env")


@dataclass(slots=True)
class Settings:
    app_name: str = "PowerBot"
    app_env: str = "development"
    app_version: str = "1.0.0"
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: list[str] = field(default_factory=lambda: ["*"])

    openai_api_key: str | None = None
    paid_api2: str | None = None

    model_path: Path = REPO_ROOT / "artifacts" / "detection_pipeline.pkl"
    vectorstore_dir: Path = REPO_ROOT / "artifacts" / "vectorstore"
    data_dir: Path = REPO_ROOT / "data"
    raw_data_path: Path = REPO_ROOT / "data" / "raw" / "merged_dataset.csv"
    rag_docs_dir: Path = REPO_ROOT / "data" / "raw" / "docs"
    log_level: str = "INFO"

    @property
    def resolved_openai_api_key(self) -> str | None:
        return self.openai_api_key or self.paid_api2


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    origins = os.getenv("CORS_ORIGINS", "*")
    return Settings(
        app_name=os.getenv("APP_NAME", "PowerBot"),
        app_env=os.getenv("APP_ENV", "development"),
        app_version=os.getenv("APP_VERSION", "1.0.0"),
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        cors_origins=[origin.strip() for origin in origins.split(",") if origin.strip()],
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        paid_api2=os.getenv("PAID_API2") or os.getenv("paid_api2"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
    )
