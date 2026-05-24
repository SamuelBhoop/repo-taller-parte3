from contextlib import asynccontextmanager

from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from app.database import get_image, init_db, insert_image
from app.s3_service import generate_presigned_url, object_exists, upload_image
from app.schemas import ImageUploadResponse, ImageUrlResponse
from app.validators import validate_image


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Taller AWS - API de imágenes",
    description="POST: sube imagen a S3 y registra en RDS. GET: URL prefirmada.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/imagenes", response_model=ImageUploadResponse, status_code=201)
async def upload_image_endpoint(
    usuario: str = Form(..., description="Nombre de usuario"),
    archivo: UploadFile = File(..., description="Imagen PNG, JPG o JPEG"),
):
    if not usuario.strip():
        raise HTTPException(status_code=400, detail="El usuario no puede estar vacío.")

    if not archivo.filename:
        raise HTTPException(status_code=400, detail="Debe enviar un archivo de imagen.")

    try:
        validate_image(archivo.filename, archivo.content_type)
    except ValueError as exc:
        raise HTTPException(status_code=415, detail=str(exc)) from exc

    content = await archivo.read()
    if not content:
        raise HTTPException(status_code=400, detail="El archivo está vacío.")

    nombre_archivo = archivo.filename
    content_type = archivo.content_type or "application/octet-stream"

    try:
        ruta_s3 = upload_image(content, content_type, usuario, nombre_archivo)
        row = insert_image(usuario, nombre_archivo, ruta_s3)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error al guardar la imagen: {exc}") from exc

    return ImageUploadResponse(**row)


@app.get("/imagenes/{usuario}/{nombre_archivo}", response_model=ImageUrlResponse)
def get_image_url(usuario: str, nombre_archivo: str):
    row = get_image(usuario, nombre_archivo)
    if row is None:
        raise HTTPException(
            status_code=404,
            detail=f"No existe la imagen '{nombre_archivo}' para el usuario '{usuario}'.",
        )

    ruta_s3 = row["ruta_s3"]
    if not object_exists(ruta_s3):
        raise HTTPException(
            status_code=404,
            detail=f"La imagen '{nombre_archivo}' del usuario '{usuario}' no está en S3.",
        )

    url = generate_presigned_url(ruta_s3)
    return ImageUrlResponse(
        usuario=row["usuario"],
        nombre_archivo=row["nombre_archivo"],
        url=url,
        fecha_almacenamiento=row["fecha_creacion"],
    )
