from pydantic import BaseModel


class BaseUpdateUser(BaseModel):
    user_id: str


class UpdateUserPassword(BaseUpdateUser):
    password: str


class UpdateOnboardingPermission(BaseUpdateUser):
    first_login: bool


class UpdateUserPhone(BaseUpdateUser):
    phone: str


class UpdateUserMessage(BaseUpdateUser):
    message: str


class UpdateUserEmail(BaseUpdateUser):
    email: str


class UpdateUserPlate(BaseUpdateUser):
    plate: str


class UpdateUserTelegram(BaseUpdateUser):
    telegram: str


class UpdateUserTelegramPermission(BaseUpdateUser):
    permission: bool


class UpdateUserWhatsappPermission(BaseUpdateUser):
    permission: bool


class UpdateUserPhonePermission(BaseUpdateUser):
    permission: bool


class UpdateUserNamePermission(BaseUpdateUser):
    permission: bool


class UpdateUserSMSPermission(BaseUpdateUser):
    permission: bool
