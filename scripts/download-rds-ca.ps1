$OutFile = Join-Path $PSScriptRoot "..\global-bundle.pem"
$Url = "https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem"

Invoke-WebRequest -Uri $Url -OutFile $OutFile
Write-Host "Certificado guardado en: $OutFile"
