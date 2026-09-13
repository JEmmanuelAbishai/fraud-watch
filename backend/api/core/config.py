from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    environment: str = "development"

    # Relational DB 
    database_url: str = "sqlite:///./fraud.db"

    # Supabase auth
    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_jwt_secret: str = "changeme"

    # GNN
    model_checkpoint_path: str = "app/ml/models/checkpoints/gnn_model.pt"

    # Neo4j
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "changeme"

    # CORS
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]


@lru_cache
def get_settings() -> Settings:
    return Settings()
