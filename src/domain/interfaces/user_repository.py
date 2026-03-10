from abc import ABC, abstractmethod

from domain.interfaces import IBaseRepository
from domain.entities import User


class IUserRepository(IBaseRepository[User], ABC):
    pass
