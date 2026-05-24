# Taller AWS — Parte 3: API de imágenes (FastAPI + S3 + RDS + Lambda)

Repositorio: https://github.com/SamuelBhoop/repo-taller-parte3

- **S3:** `user-1138025476-ueia-so` (`us-east-1`)
- **RDS:** PostgreSQL `taller-aws`
- **Endpoint:** `taller-aws.c2l8uo4wgjp3.us-east-1.rds.amazonaws.com`

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/imagenes` | `usuario` + archivo (form-data). Sube a S3 y guarda en RDS |
| GET | `/imagenes/{usuario}/{nombre_archivo}` | URL prefirmada + fecha de almacenamiento |
| GET | `/health` | Estado del servicio |
| GET | `/docs` | Swagger UI |

Formatos permitidos: **PNG, JPG, JPEG** (error **415** si no).

---

## Paso 1 — Tú: terminar RDS

1. Espera que `taller-aws` quede en estado **Available**.
2. En RDS → instancia → **Connectivity** copia:
   - **Endpoint**
   - **Port** (5432)
   - Usuario y contraseña maestros que definiste al crear la BD
3. En **Modify** activa **Publicly accessible = Yes** si vas a probar desde tu PC o Lambda **sin VPC** (más simple para el taller).
4. Guarda el Security Group con **5432** (ya lo tienes).

## Paso 2 — Tú: archivo `.env` (no subir a GitHub)

Copia `.env.example` a `.env` y completa:

```env
AWS_REGION=us-east-1
S3_BUCKET=user-1138025476-ueia-so

DB_HOST=taller-aws.c2l8uo4wgjp3.us-east-1.rds.amazonaws.com
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=tu_password
DB_SSLMODE=verify-full
DB_SSLROOTCERT=global-bundle.pem
```

Credenciales AWS en tu PC (`aws configure`) o variables `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` con permisos sobre el bucket S3.

## Paso 2b — Certificado SSL de RDS (como en la consola AWS)

En la raíz del proyecto:

```powershell
.\scripts\download-rds-ca.ps1
```

Equivale a:

```powershell
curl -o global-bundle.pem https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem
```

El archivo `global-bundle.pem` no se sube a GitHub (está en `.gitignore`). Docker y Lambda lo descargan al construir la imagen.

Si SSL falla en pruebas locales, en `.env` pon temporalmente: `DB_SSLMODE=disable`

## Paso 3 — Tú: probar en local

Usa **Python 3.11 o 3.12** (en Windows evita 3.14 si `pip` falla con drivers de BD).

```powershell
cd C:\Users\User\repo-taller-parte3
git pull
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Abre http://127.0.0.1:8000/docs → prueba **POST /imagenes** y **GET /imagenes/{usuario}/{nombre_archivo}**.

La tabla `imagenes` se crea sola al arrancar (también puedes ejecutar `sql/schema.sql` en RDS).

## Paso 4 — Tú: Docker (parte c)

```powershell
docker build -t taller-api:local .
docker run --rm -p 8000:8000 --env-file .env taller-api:local
```

## Paso 5 — Tú: ECR (parte d)

1. ECR → **Create repository** → nombre ej. `taller-fastapi-imagenes`
2. Usa los comandos de **View push commands** con `Dockerfile.lambda`:

```powershell
docker build -f Dockerfile.lambda -t taller-fastapi-imagenes .
# tag y push según ECR
```

O edita `scripts/ecr-push.ps1` con tu Account ID.

## Paso 6 — Tú: Lambda (parte e)

1. **Create function** → **Container image** → imagen de ECR
2. Variables de entorno (mismas que `.env`)
3. Rol IAM: `s3:PutObject`, `s3:GetObject`, `s3:HeadObject` en el bucket; si RDS en VPC, Lambda en la misma VPC + SG que permita 5432
4. **Configuration → Function URL** → crear URL pública
5. Probar: `https://xxxxx.lambda-url.us-east-1.on.aws/docs`

Timeout recomendado: **30 s**, memoria **512 MB+**.

## Evidencias (capturas)

- POST /imagenes exitoso
- GET con URL prefirmada
- Objeto en S3 (`usuario/archivo.jpg`)
- Tabla `imagenes` en RDS
- `docker build` / `docker run`
- Repositorio ECR con imagen
- Lambda + Function URL

## Estructura

```
app/           # Código FastAPI
sql/           # Schema PostgreSQL
Dockerfile     # Local / pruebas
Dockerfile.lambda  # ECR + Lambda
lambda_handler.py  # Mangum
scripts/       # Ayuda ECR
```
