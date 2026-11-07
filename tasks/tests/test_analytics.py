import pytest
from django.utils import timezone
from datetime import timedelta

from employees.models import Employee
from tasks.models import Task


@pytest.fixture
def employees(db):
    return [
        Employee.objects.create(full_name=f"Сотрудник {i}", position="Разработчик",
                                email=f"e{i}@example.com")
        for i in range(3)
    ]


@pytest.fixture
def task(db, employees):
    return Task.objects.create(title="Тестовая задача",
                               due_date=timezone.localdate() + timedelta(days=3))


def test_suggest_least_loaded(api_client, employees, task):
    # первая задача — первому сотруднику
    task.assignee = employees[0]
    task.save()

    # вторая задача, исполнителя нет — должны предложить второго (0 задач)
    resp = api_client.get(f"/api/tasks/{task.id}/suggest_assignee/")
    assert resp.status_code == 200
    assert resp.data["suggested_assignee_id"] == employees[1].id


def test_workload_ordering(api_client, employees):
    Employee.objects.create(full_name="Занятый", position="Разработчик",
                            email="busy@example.com", is_active=True)
    busy = Employee.objects.get(email="busy@example.com")
    for _ in range(3):
        Task.objects.create(title=f"Задача {busy.id}",
                            assignee=busy,
                            due_date=timezone.localdate() + timedelta(days=1))

    resp = api_client.get("/api/employees/workload/")
    data = resp.json()
    assert data[0]["open_tasks"] == 0
    assert data[-1]["open_tasks"] == 3
