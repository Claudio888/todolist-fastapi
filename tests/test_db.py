from dataclasses import asdict

from sqlalchemy import select

from todolist.models import Task


def test_create_task(session, mock_db_time):
    with mock_db_time(model=Task) as time:
        new_task = Task(
            task_name='Ida ao Mercado',
            task_description='Comprar macarrao',
            task_priority=1,
        )
        session.add(new_task)
        session.commit()

        task = session.scalar(
            select(Task).where(Task.task_name == 'Ida ao Mercado')
        )

    assert asdict(task) == {
        'id': 1,
        'task_name': 'Ida ao Mercado',
        'task_description': 'Comprar macarrao',
        'task_priority': 1,
        'created_at': time,
    }
