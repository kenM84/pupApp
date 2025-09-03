from abc import ABC, abstractmethod
from typing import Optional


class GenericSecretProvider(ABC):
    """
    Abstract base class for secret providers.
    """

    @abstractmethod
    def configure(self) -> bool:
        """
        Initializes the secret provider and verifies connectivity.
        """
        pass

    @abstractmethod
    def get_secret(self, secret_name: str) -> Optional[str]:
        """
        Fetches a secret by name.
        """
        pass
