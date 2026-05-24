CREATE TABLE IF NOT EXISTS imagenes (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(255) NOT NULL,
    nombre_archivo VARCHAR(512) NOT NULL,
    ruta_s3 TEXT NOT NULL UNIQUE,
    fecha_creacion TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_imagenes_usuario_nombre
    ON imagenes (usuario, nombre_archivo);
