from pydantic import BaseModel


class BaseUpdateUser(BaseModel):
    user_id: str


class UpdateUserPhone(BaseUpdateUser):
    phone: str


class UpdateUserMessage(BaseUpdateUser):
    message: str


class UpdateUserEmail(BaseUpdateUser):
    email: str


class UpdateUserPassword(BaseUpdateUser):
    password: str


class UpdateUserPlate(BaseUpdateUser):
    plate: str
