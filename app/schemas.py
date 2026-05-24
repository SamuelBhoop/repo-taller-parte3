from datetime import datetime

from pydantic import BaseModel, Field


class ImageUploadResponse(BaseModel):
    id: int
    usuario: str
    nombre_archivo: str
    ruta_s3: str = Field(description="Ruta del objeto en el bucket S3")
    fecha_creacion: datetime


class ImageUrlResponse(BaseModel):
    usuario: str
    nombre_archivo: str
    url: str = Field(description="URL prefirmada para acceder a la imagen")
    fecha_almacenamiento: datetime
