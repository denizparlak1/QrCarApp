from pydantic import BaseModel


class UserRegistration(BaseModel):
    email: str
    password: str
