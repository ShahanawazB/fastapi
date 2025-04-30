from fastapi import FastAPI, Depends ,HTTPException, Path,Query
import sqlalchemy
from starlette import status
import models
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import Todos
from pydantic import BaseModel, Field

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally :
        db.close()



db_dependency = Annotated[Session, Depends(get_db)]

class TodosRequest(BaseModel):
    title :str = Field(min_length=3)
    description :str = Field(min_length= 5, max_length=100)
    priority : int = Field (gt=0, lt=6)
    complete :bool

@app.get('/', status_code= status.HTTP_200_OK)
async def get_all(db : db_dependency ):
    return db.query(Todos).all()

@app.get('/todos/{id}', status_code= status.HTTP_200_OK)
async def get_record(db : db_dependency, id : int = Path(gt=0)):
    todo_modal = db.query(Todos).filter(Todos.id == id).first()
    if todo_modal is not None:
        return todo_modal
    return HTTPException(status_code=404, detail="The requested data not found")

@app.post('/todo', status_code=status.HTTP_201_CREATED)
async def create_record(db : db_dependency, new_record : TodosRequest):
    todo_modal = Todos(**new_record.model_dump())
    db.add(todo_modal)
    db.commit()

@app.put("/todo/{id}",status_code=status.HTTP_204_NO_CONTENT)
def update_record(db : db_dependency, new_record : TodosRequest, id : int = Path(gt=0)):
    todo_modal = db.query(Todos).filter(Todos.id == id).first()
    if todo_modal is None:
        raise HTTPException(status_code=404, detail="detail requested not found")
    todo_modal.title = new_record.title
    todo_modal.description = new_record.description
    todo_modal.priority = new_record.priority
    todo_modal.complete = new_record.complete

    db.add(todo_modal)
    db.commit()

@app.delete("/todos/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_record (db : db_dependency,id : int = Path(gt=0)):
    todo_modal = db.query(Todos).filter(Todos.id == id).first()
    if todo_modal is None:
        raise HTTPException(status_code=404, detail="detail requested not found")
    db.query(Todos).filter(Todos.id == id).delete()
    db.commit()
    