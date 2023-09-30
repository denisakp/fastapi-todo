from fastapi import Depends, FastAPI, HTTPException, status, Response
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_database, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/", description="Load todo list", response_model=list[schemas.Todo])
def get_todos(
    db: Session = Depends(get_database),
    state: bool = False,
    page: int = 1,
    limit: int = 15,
):
    skip = (page - 1) * limit

    todos = (
        db.query(models.Todo)
        .filter(models.Todo.is_done == state)
        .limit(limit)
        .offset(skip)
        .all()
    )
    return todos


@app.get("/{id}", description="Load a Todo by its Id", response_model=schemas.Todo)
def get_todo(id: int, db: Session = Depends(get_database)):
    todo = db.query(models.Todo).filter(models.Todo.id == id).first()

    if todo is None:
        raise HTTPException(status_code=404, detail="Resource Not Found")
    return todo


@app.post("/", description="Create a new Todo", response_model=schemas.Todo)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_database)):
    new_todo = models.Todo(**todo.dict())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


@app.patch("/{id}", description="Update Todo", response_model=schemas.Todo)
def update_todo(
    id: int, schema: schemas.TodoCreate, db: Session = Depends(get_database)
):
    todo_query = db.query(models.Todo).filter(models.Todo.id == id)
    db_todo = todo_query.first()

    if todo_query is None:
        raise HTTPException(status_code=404, detail="Resource Not Found")

    todo_query.filter(models.Todo.id == id).update(
        schema.dict(), synchronize_session=False
    )
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.delete("/{id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_database)):
    todo_query = db.query(models.Todo).filter(models.Todo.id == todo_id)
    db_todo = todo_query.first()

    if not db_todo:
        raise HTTPException(status_code=404, detail="Resource Not Found")

    todo_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
