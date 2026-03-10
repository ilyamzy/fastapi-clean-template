import logging

from firebase_admin import auth

from domain.interfaces.auth_service import IAuthService
from application.exceptions.token import InvalidToken


logger = logging.getLogger(__name__)


class FirebaseAuthService(IAuthService):

    def verify_token(self, token: str) -> str:
        try:
            decoded_token = auth.verify_id_token(token)
            return decoded_token['uid']
        except Exception as e:
            logger.exception(e)
            raise InvalidToken
