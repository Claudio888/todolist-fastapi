from http import HTTPStatus

from fastapi.testclient import TestClient

from todolist.app import app
from todolist.schemas import TaskSchema


def test_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_task(client):
    response = client.post(
        '/tasks',
        json={
            'task_name': 'Ir ao Medico',
            'task_description': 'medico meio dia',
            'task_priority': 1,
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'task_name': 'Ir ao Medico',
        'task_description': 'medico meio dia',
        'task_priority': 1,
    }


def test_read_tasks(client):
    response = client.get('/tasks')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'tasks': []}


def test_read_tasks_when_exists(client, task):
    task_schema = TaskSchema.model_validate(task).model_dump()
    response = client.get('/tasks/')
    assert response.json() == {'tasks': [task_schema]}


def test_update_task(client, task):
    response = client.put(
        '/tasks/1',
        json={
            'task_name': 'Entrevista Emprego',
            'task_description': 'Fazer entrevista xyz',
            'task_priority': 1,
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'task_name': 'Entrevista Emprego',
        'task_description': 'Fazer entrevista xyz',
        'task_priority': 1,
    }


def test_delete_task(client, task):
    response = client.delete('/tasks/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Task Deleted'}


def test_delete_task_nonexists(client):
    response = client.delete('/task/999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Not Found'}


def test_update_task_nonexists(client):
    response = client.put(
        '/task/1111',
        json={
            'task_name': 'Ir ao medico',
            'task_description': 'meio dia',
            'task_priority': 1,
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Not Found'}


def test_get_task_by_id(client, task):
    response = client.get(f'/tasks/{task.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'task_name': task.task_name,
        'task_description': task.task_description,
        'task_priority': task.task_priority,
    }


def test_get_task_by_id_not_found(client):
    response = client.get('/task/999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Not Found'}
