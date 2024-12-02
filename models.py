from pydantic import BaseModel
from typing import List
from enum import Enum


class BookData(BaseModel):
    title: str
    picture: str
    rows: List[dict]

class SearchType(Enum):
    AllFields = "AllFields"
    Title = "Title"
    Author = "Author"
    Subject = "Subject"
    ISBN = "ISN"