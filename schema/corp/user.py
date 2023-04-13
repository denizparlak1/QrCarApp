from pydantic import BaseModel


class GetQrData(BaseModel):
    corp_name: str


class CreateUser(BaseModel):
    corporation_name: str
    name: str
    surname: str
    phone: int
    mail: str


class DeleteUser(BaseModel):
    corporation_name: str
    user_id: int


class CreateCorporationAdmin(BaseModel):
    corporation_name: str
    email: str
    password: str
    role: str


class ListCorporationUser(BaseModel):
    corporation_name: str
