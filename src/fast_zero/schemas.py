from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class User(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserDB(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str


class UserList(BaseModel):
    users: list[UserPublic]
