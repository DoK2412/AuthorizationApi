from pydantic import BaseModel

from datetime import datetime

class UserRole(BaseModel):
    id: int
    type: str


class User(BaseModel):
    id: int
    name: str
    password: str
    email: str
    active: bool
    number: str | None = None
    number_active: bool
    create_date: datetime
    update_date: datetime  | None = None
    blocking: bool
    blocking_data: datetime  | None = None
    role: int