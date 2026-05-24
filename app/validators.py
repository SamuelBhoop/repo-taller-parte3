ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg"}
ALLOWED_CONTENT_TYPES = {
    "image/png",
    "image/jpeg",
    "image/jpg",
}


def validate_image(filename: str, content_type: str | None) -> None:
    lower_name = filename.lower()
    if not any(lower_name.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise ValueError("Formato no permitido. Use PNG, JPG o JPEG.")

    if content_type and content_type.lower() not in ALLOWED_CONTENT_TYPES:
        raise ValueError("Content-Type no permitido. Use image/png o image/jpeg.")
