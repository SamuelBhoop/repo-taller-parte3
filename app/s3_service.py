import boto3
from botocore.exceptions import ClientError

from app.config import settings

_s3 = boto3.client("s3", region_name=settings.aws_region)


def build_s3_key(usuario: str, nombre_archivo: str) -> str:
    return f"{usuario.strip()}/{nombre_archivo}"


def upload_image(file_bytes: bytes, content_type: str, usuario: str, nombre_archivo: str) -> str:
    key = build_s3_key(usuario, nombre_archivo)
    _s3.put_object(
        Bucket=settings.s3_bucket,
        Key=key,
        Body=file_bytes,
        ContentType=content_type,
    )
    return key


def generate_presigned_url(ruta_s3: str) -> str:
    return _s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.s3_bucket, "Key": ruta_s3},
        ExpiresIn=settings.presigned_url_expiration,
    )


def object_exists(ruta_s3: str) -> bool:
    try:
        _s3.head_object(Bucket=settings.s3_bucket, Key=ruta_s3)
        return True
    except ClientError:
        return False
