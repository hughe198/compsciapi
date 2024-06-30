from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import SessionLocal, engine

app = FastAPI()

origins = [
    "http://127.0.0.1",
    "http://localhost:4200",
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/projects/", response_model=schemas.Project, status_code=status.HTTP_201_CREATED)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    db_project = models.Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@app.get("/projects/", response_model=List[schemas.Project])
def read_projects(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    projects = db.query(models.Project).offset(skip).limit(limit).all()
    return projects

@app.get("/projects/{project_id}", response_model=schemas.Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project 

@app.post("/projects/{project_id}/pages/", response_model=schemas.Page, status_code = status.HTTP_201_CREATED)
def create_page_for_project(project_id: int, page: schemas.PageCreate, db: Session = Depends(get_db)):
    db_page = models.Page(**page.dict(), project_id=project_id)
    db.add(db_page)
    db.commit()
    db.refresh(db_page)
    return db_page

@app.get("/pages/", response_model=List[schemas.Page])
def read_pages(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    pages = db.query(models.Page).offset(skip).limit(limit).all()
    return pages

@app.get("/pages/{page_id}", response_model=schemas.Page)
def read_page(page_id: int, db: Session = Depends(get_db)):
    page = db.query(models.Page).filter(models.Page.id == page_id).first()
    if page is None:
        raise HTTPException(status_code=404, detail="Page not found")
    return page

@app.get("/projects/{project_id}/pages/", response_model=List[schemas.Page])
def get_pages_by_project_id(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    pages = db.query(models.Page).filter(models.Page.project_id == project_id).all()
    return pages