from pydantic import BaseModel
from datetime import datetime


class TodoBase(BaseModel):
    title: str
    description: str | None = None


class TodoCreate(TodoBase):
    pass


class Todo(TodoBase):
    id: int
    is_done: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True
