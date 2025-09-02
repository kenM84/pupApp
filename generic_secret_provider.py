# This is a copy of the generic secret provider for Azure deployment
# Azure App Service seems to have issues with subdirectories

from abc import ABC, abstractmethod
from typing import Optional


class GenericSecretProvider(ABC):
    """
    Abstract base class for secret providers.
    """

    @abstractmethod
    async def configure(self) -> bool:
        """
        Initializes the secret provider and verifies connectivity.
        """
        pass

    @abstractmethod
    async def get_secret(self, secret_name: str) -> Optional[str]:
        """
        Fetches a secret by name.
        """
        pass
