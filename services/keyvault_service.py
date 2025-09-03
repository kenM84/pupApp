# This is a copy of the keyvault service for Azure deployment
# Azure App Service seems to have issues with subdirectories

import logging
import os
from typing import Dict, Optional

from azure.keyvault.secrets import SecretClient
from azure.keyvault.secrets import KeyVaultSecret
from fastapi.security import APIKeyHeader
from azure.identity import DefaultAzureCredential

from .generic_secret_provider import GenericSecretProvider


class KeyVaultService(GenericSecretProvider):
    """
    Implementation of GenericSecretProvider that fetches secrets from Azure
    Key Vault.
    """

    def __init__(self):
        self.logger = logging.getLogger("default-logger")
        self.envCred = DefaultAzureCredential()
        self.cred_cache: Dict[str, str] = {}
        self.iterable_creds: Dict[str, int] = {}
        self.api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

        vault_name = os.environ.get("KeyVaultName")
        if not vault_name:
            self.logger.warning("KeyVaultName environment variable not set.")
        self.keyVaultUrl = f"https://{vault_name}.vault.azure.net/"

    def configure(self) -> bool:
        """
        Initializes the SecretClient and verifies connectivity.
        """
        try:
            # Test connectivity by creating a client and attempting to list
            # secrets
            client = SecretClient(self.keyVaultUrl, self.envCred)
            # Try to list secrets to verify connectivity
            # (this will fail if no permissions, but that's ok)
            list(client.list_properties_of_secrets(max_page_size=1))
            self.logger.debug(
                f"KeyVaultService initialized with URL: {self.keyVaultUrl}")
            return True
        except Exception:
            self.logger.error("Failed to configure KeyVaultService.",
                              exc_info=True)
            return False

    def get_secret(self, secret_name: str) -> Optional[str]:
        """
        Fetches a secret from environment variables or Azure Key Vault.
        """
        try:
            # Check if secret is available in environment
            if os.environ.get(secret_name):
                return os.environ.get(secret_name)

            underscore_secret = secret_name.replace("-", "_")
            if os.environ.get(underscore_secret):
                return os.environ.get(underscore_secret)

            client = SecretClient(self.keyVaultUrl, self.envCred)
            secret = client.get_secret(secret_name)
            return self.split_secret_if_array(secret)
        except Exception:
            self.logger.error(f"Error retrieving secret '{secret_name}'.",
                              exc_info=True)
            return None

    def split_secret_if_array(self, secret: Optional[KeyVaultSecret]) -> \
            Optional[str]:
        """
        Splits a secret string by '|' and rotates over segments if multiple
        exist.
        """
        if not secret:
            self.logger.debug("split_secret_if_array: Received None secret.")
            return None

        secret_value = secret.value
        secret_segments = secret_value.split("|")
        cred_count = len(secret_segments)

        if cred_count > 1:
            iteration_num = self.iterable_creds.get(secret_value, 0)
            self.iterable_creds[secret_value] = \
                (iteration_num + 1) % cred_count
            self.logger.debug(
                f"Rotating secret segment: current={iteration_num}, "
                f"next={self.iterable_creds[secret_value]}")
            return secret_segments[iteration_num]
        return secret_value
