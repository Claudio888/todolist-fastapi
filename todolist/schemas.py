from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TaskFull(BaseModel):
    id: int
    task_name: str
    task_description: str
    task_priority: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class TaskSchema(BaseModel):
    task_name: str
    task_description: str
    task_priority: int
    model_config = ConfigDict(from_attributes=True)


class TaskList(BaseModel):
    tasks: list[TaskFull]


class Message(BaseModel):
    message: str
