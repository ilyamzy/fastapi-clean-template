from abc import ABC, abstractmethod


class IAuthService(ABC):

    @abstractmethod
    async def verify_token(self, token: str) -> str:
        raise NotImplementedError
