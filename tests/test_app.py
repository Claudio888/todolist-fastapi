from http import HTTPStatus

from fastapi.testclient import TestClient

from todolist.app import app
from todolist.models import Task
from todolist.schemas import TaskSchema


def test_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_task(client: TestClient):
    response = client.post(
        '/tasks',
        json={
            'task_name': 'Ir ao Medico',
            'task_description': 'medico meio dia',
            'task_priority': 1,
        },
    )
    assert response.status_code == HTTPStatus.CREATED

    response_json = response.json()

    assert response_json['task_name'] == 'Ir ao Medico'
    assert response_json['task_description'] == 'medico meio dia'
    assert response_json['task_priority'] == 1

    assert 'id' in response_json
    assert 'created_at' in response_json


def test_read_tasks(client: TestClient):
    response = client.get('/tasks')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'tasks': []}


def test_read_tasks_when_exists(session, client, task):
    TaskSchema.model_validate(task).model_dump()

    response = client.get('/tasks/')

    response_json = response.json()

    assert response_json['tasks'][0]['task_name'] == 'Medico hoje'
    assert response_json['tasks'][0]['task_description'] == 'Otorrino hoje'
    assert response_json['tasks'][0]['task_priority'] == 1

    assert 'id' in response_json['tasks'][0]
    assert 'created_at' in response_json['tasks'][0]


def test_update_task(client: TestClient, task: Task):
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


def test_delete_task(client: TestClient, task: Task):
    response = client.delete('/tasks/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Task Deleted'}


def test_delete_task_nonexists(client: TestClient):
    response = client.delete('/task/999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Not Found'}


def test_update_task_nonexists(client: TestClient):
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


def test_get_task_by_id(client: TestClient, task: Task):
    response = client.get(f'/tasks/{task.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'task_name': task.task_name,
        'task_description': task.task_description,
        'task_priority': task.task_priority,
    }


def test_get_task_by_id_not_found(client: TestClient):
    response = client.get('/task/999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Not Found'}
