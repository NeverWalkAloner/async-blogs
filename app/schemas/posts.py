from datetime import datetime

from pydantic import BaseModel


class PostModel(BaseModel):
    """ Validate request data """
    title: str
    content: str


class PostDetailsModel(PostModel):
    """ Return response data """
    id: int
    created_at: datetime
    user_name: str
