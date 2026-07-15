from app.config import settings


class AuthorizationService:

    def is_authorized(
        self,
        phone_number: str
    ) -> bool:

        print("Incoming:", repr(phone_number))
        print("Allowed:", settings.allowed_users)

        return phone_number in settings.allowed_users


authorization_service = AuthorizationService()