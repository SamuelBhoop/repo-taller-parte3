# Ajusta ACCOUNT_ID, REPO_NAME y REGION antes de ejecutar.
$ACCOUNT_ID = "TU_ACCOUNT_ID"
$REGION = "us-east-1"
$REPO_NAME = "taller-fastapi-imagenes"
$IMAGE_TAG = "latest"

$ECR_URI = "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO_NAME"

aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com"

docker build -f Dockerfile.lambda -t "${REPO_NAME}:${IMAGE_TAG}" .
docker tag "${REPO_NAME}:${IMAGE_TAG}" "${ECR_URI}:${IMAGE_TAG}"
docker push "${ECR_URI}:${IMAGE_TAG}"

Write-Host "Imagen subida: ${ECR_URI}:${IMAGE_TAG}"
