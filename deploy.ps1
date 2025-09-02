# Change these values to the ones used to create the App Service.
$RESOURCE_GROUP_NAME = 'kmillard84_rg_8256'
$APP_SERVICE_NAME = 'kind-tree-945d797a4d904dab8134f756a9d9b2fd'

# Create deployment zip file
$ZIP_FILE = 'deployment.zip'

Write-Host "Starting deployment process..."

# Remove existing zip file if it exists
if (Test-Path $ZIP_FILE) {
    Write-Host "Removing existing deployment package..."
    Remove-Item $ZIP_FILE
}

# Create zip file with necessary files for deployment
Write-Host "Creating deployment package..."
$filesToZip = @('app.py', 'requirements.txt', 'static', 'templates', 'services', '__init__.py', 'startup.py', 'web.config', 'gunicorn.conf.py', 'startup.sh', 'diagnose.py', 'keyvault_service.py', 'generic_secret_provider.py')

try {
    Compress-Archive -Path $filesToZip -DestinationPath $ZIP_FILE -Force
    Write-Host "✅ Created deployment package: $ZIP_FILE"
}
catch {
    Write-Host "❌ Failed to create deployment package: $($_.Exception.Message)"
    exit 1
}

# Deploy to Azure
Write-Host "Deploying to Azure..."
try {
    az webapp deploy --name $APP_SERVICE_NAME --resource-group $RESOURCE_GROUP_NAME --src-path $ZIP_FILE
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Deployment successful!"
    } else {
        Write-Host "❌ Deployment failed"
        exit 1
    }
}
catch {
    Write-Host "❌ Deployment failed: $($_.Exception.Message)"
    exit 1
}
