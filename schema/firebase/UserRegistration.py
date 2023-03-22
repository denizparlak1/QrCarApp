from pydantic import BaseModel


class UserRegistration(BaseModel):
    email: str
    password: str
    role: str


class BulkRegisterRequest(BaseModel):
    customer: str
    count: int
    role: str
