from pydantic import BaseModel, ConfigDict


class TaskSchema(BaseModel):
    task_name: str
    task_description: str
    task_priority: int
    model_config = ConfigDict(from_attributes=True)


class TaskList(BaseModel):
    tasks: list[TaskSchema]


class Message(BaseModel):
    message: str
