from pathlib import Path

import psycopg2
from psycopg2.extras import RealDictCursor

from app.config import settings


def _connection_kwargs() -> dict:
    kwargs: dict = {
        "host": settings.db_host,
        "port": settings.db_port,
        "dbname": settings.db_name,
        "user": settings.db_user,
        "password": settings.db_password,
        "cursor_factory": RealDictCursor,
    }

    sslmode = (settings.db_sslmode or "").strip().lower()
    if sslmode and sslmode != "disable":
        kwargs["sslmode"] = settings.db_sslmode
        cert_path = Path(settings.db_sslrootcert)
        if not cert_path.is_file():
            raise FileNotFoundError(
                f"No se encontró el certificado RDS en '{cert_path}'. "
                "Ejecuta: .\\scripts\\download-rds-ca.ps1"
            )
        kwargs["sslrootcert"] = str(cert_path)

    return kwargs


def get_connection():
    return psycopg2.connect(**_connection_kwargs())


def init_db() -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS imagenes (
                    id SERIAL PRIMARY KEY,
                    usuario VARCHAR(255) NOT NULL,
                    nombre_archivo VARCHAR(512) NOT NULL,
                    ruta_s3 TEXT NOT NULL UNIQUE,
                    fecha_creacion TIMESTAMPTZ NOT NULL DEFAULT NOW()
                );
                CREATE INDEX IF NOT EXISTS idx_imagenes_usuario_nombre
                    ON imagenes (usuario, nombre_archivo);
                """
            )
        conn.commit()


def insert_image(usuario: str, nombre_archivo: str, ruta_s3: str) -> dict:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO imagenes (usuario, nombre_archivo, ruta_s3)
                VALUES (%s, %s, %s)
                RETURNING id, usuario, nombre_archivo, ruta_s3, fecha_creacion
                """,
                (usuario, nombre_archivo, ruta_s3),
            )
            row = cur.fetchone()
        conn.commit()
    return dict(row)


def get_image(usuario: str, nombre_archivo: str) -> dict | None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, usuario, nombre_archivo, ruta_s3, fecha_creacion
                FROM imagenes
                WHERE usuario = %s AND nombre_archivo = %s
                """,
                (usuario, nombre_archivo),
            )
            row = cur.fetchone()
    return dict(row) if row else None
