from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

from todolist.database import get_session
from todolist.models import Task
from todolist.schemas import Message, TaskFull, TaskList, TaskSchema

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}


@app.post('/tasks/', status_code=HTTPStatus.CREATED, response_model=TaskFull)
def create_user(task: TaskSchema, session: Session = Depends(get_session)):
    new_task = Task(
        task_name=task.task_name,
        task_description=task.task_description,
        task_priority=task.task_priority,
    )

    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    return new_task


@app.get('/tasks/', status_code=HTTPStatus.OK, response_model=TaskList)
def read_tasks(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    tasks = session.scalars(select(Task).offset(skip).limit(limit)).all()

    return {'tasks': tasks}


@app.get('/tasks/{task_id}', response_model=TaskSchema)
def read_one_task(task_id: int, session: Session = Depends(get_session)):
    task_db = session.scalar(select(Task).where(Task.id == task_id))

    if not task_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Not Found'
        )

    return task_db


@app.put('/tasks/{task_id}', response_model=TaskSchema)
def update_task(
    task_id: int, task: TaskSchema, session: Session = Depends(get_session)
):
    task_db = session.scalar(select(Task).where(Task.id == task_id))
    if not task_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Not Found'
        )

    task_db.task_name = task.task_name
    task_db.task_description = task.task_description
    task_db.task_priority = task.task_priority
    session.commit()
    session.refresh(task_db)

    return task_db


@app.delete('/tasks/{task_id}', response_model=Message)
def delete_task(task_id: int, session: Session = Depends(get_session)):
    task_db = session.scalar(select(Task).where(Task.id == task_id))

    if not task_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Not Found'
        )

    session.delete(task_db)
    session.commit()

    return {'message': 'Task Deleted'}
