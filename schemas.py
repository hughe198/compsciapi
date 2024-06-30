from pydantic import BaseModel
from typing import List, Optional

class PageBase(BaseModel):
    title: str
    content: str

class PageCreate(PageBase):
    pass

class Page(PageBase):
    id: int
    project_id: int

    class Config:
        orm_mode = True

class ProjectBase(BaseModel):
    title: str
    description: str
    thumbnail_url: str
    project_catagory: str
    
class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    pages: List[Page] = []

    class Config:
        orm_mode = True
