from infrastructure.db.mappers import BaseMapper
from infrastructure.db.models import UserModel
from domain.entities import User


class UserMapper(BaseMapper):
    
    @staticmethod
    def to_domain(model: UserModel) -> User:
        return User(
            id=model.id
        )

    @staticmethod
    def to_model(domain: User) -> UserModel:
        return UserModel(
            id=domain.id
        )
