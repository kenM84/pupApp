import logging
from azure.storage.blob import BlobServiceClient, BlobClient
import requests

from .keyvault_service import KeyVaultService

logger = logging.getLogger("default-logger")

genaisys_blob_service_client = None  # explicitly declare global client


def configure():
    global genaisys_blob_service_client
    try:
        keyvault_service = KeyVaultService()
        account_name = keyvault_service.get_secret("Storage--AccountName")
        key = keyvault_service.get_secret("Storage--AccessKey")
        connect_str = (
            f"DefaultEndpointsProtocol=https;"
            f"AccountName={account_name};"
            f"AccountKey={key};"
            f"EndpointSuffix=core.windows.net"
        )

        genaisys_blob_service_client = (
            BlobServiceClient.from_connection_string(connect_str))
        logger.debug("Genaisys blob service client configured successfully.")
    except Exception as e:
        logger.error("Error configuring blob service: %s", e, exc_info=True)
        raise RuntimeError("Error configuring blob service") from e


def download_genaisys_blob_by_http(url: str) -> str:
    """Download blob content directly via HTTP GET."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logger.error("HTTP blob download failed for URL %s: %s", url, e,
                     exc_info=True)
        raise


def download_genaisys_blob(container: str, path: str) -> bytes:
    """Download blob content from Azure Blob Storage."""
    global genaisys_blob_service_client
    if genaisys_blob_service_client is None:
        configure()

    logger.debug("Downloading blob '%s' from container '%s'.", path, container)
    container_client = genaisys_blob_service_client.get_container_client(
        container)
    blob_client: BlobClient = container_client.get_blob_client(path)
    download_stream = blob_client.download_blob()
    data = download_stream.readall()
    logger.debug("Downloaded %d bytes from blob '%s'.", len(data), path)
    return data


def upload_genaisys_blob(container: str, path: str, data) -> bool:
    """Upload blob without overwriting existing blobs."""
    global genaisys_blob_service_client
    if genaisys_blob_service_client is None:
        configure()

    logger.debug("Uploading blob '%s' to container '%s' (no overwrite).",
                 path, container)
    container_client = genaisys_blob_service_client.get_container_client(
        container)
    blob_client: BlobClient = container_client.get_blob_client(path)
    blob_client.upload_blob(data)
    logger.info("Uploaded blob '%s' to container '%s'.", path, container)
    return True


def upload_or_replace_genaisys_blob(container: str, path: str, data) -> bool:
    """Upload blob and overwrite if it exists."""
    global genaisys_blob_service_client
    if genaisys_blob_service_client is None:
        configure()

    logger.debug("Uploading blob '%s' to container '%s' with overwrite.",
                 path, container)
    container_client = genaisys_blob_service_client.get_container_client(
        container)
    blob_client: BlobClient = container_client.get_blob_client(path)
    blob_client.upload_blob(data, overwrite=True)
    logger.info("Uploaded (with overwrite) blob '%s' to container '%s'.",
                path, container)
    return True
