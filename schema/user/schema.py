from pydantic import BaseModel


class BaseUpdateUser(BaseModel):
    user_id: str


class UpdateUserPassword(BaseUpdateUser):
    password: str


class UpdateUserPhone(BaseUpdateUser):
    phone: str


class UpdateUserMessage(BaseUpdateUser):
    message: str


class UpdateUserEmail(BaseUpdateUser):
    email: str


class UpdateUserPlate(BaseUpdateUser):
    plate: str


class UpdateFullName(BaseUpdateUser):
    fullname: str


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


class DownloadQrFileURL(BaseUpdateUser):
    url: str


class NotificationMessages(BaseUpdateUser):
    message: str


class DeviceIdStore(BaseUpdateUser):
    device_id: str