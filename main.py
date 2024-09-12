from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from datetime import datetime

# Database setup
DATABASE_URL = "mssql+pyodbc://username:password@server/db?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    due_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Task model for API input/output
class TaskModel(BaseModel):
    name: str
    description: str
    due_date: str

# API Endpoints
@app.get("/tasks")
def get_tasks():
    db = SessionLocal()
    tasks = db.query(Task).all()
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks")
def create_task(task: TaskModel):
    db = SessionLocal()
    db_task = Task(name=task.name, description=task.description, due_date=task.due_date)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskModel):
    db = SessionLocal()
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.name = task.name
    db_task.description = task.description
    db_task.due_date = task.due_date
    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}
