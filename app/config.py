from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    aws_region: str = "us-east-1"
    s3_bucket: str = "user-1138025476-ueia-so"

    db_host: str = "taller-aws.c2l8uo4wgjp3.us-east-1.rds.amazonaws.com"
    db_port: int = 5432
    db_name: str = "postgres"
    db_user: str = "postgres"
    db_password: str

    # SSL RDS (como en la consola AWS: verify-full + global-bundle.pem)
    db_sslmode: str = "verify-full"
    db_sslrootcert: str = str(_ROOT / "global-bundle.pem")

    presigned_url_expiration: int = 3600


settings = Settings()
