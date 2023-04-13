from pydantic import BaseModel


class CorporationUser(BaseModel):
    id: str
    mail: str
    name: str
    surname: str
    phone: int
    username: str