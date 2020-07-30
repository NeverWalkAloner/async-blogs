from datetime import datetime

from pydantic import BaseModel


class PostModel(BaseModel):
    title: str
    content: str


class PostDetailsModel(PostModel):
    id: int
    created_at: datetime
    user_name: str
