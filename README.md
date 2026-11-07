# LoadBalance Tracker

API-сервис для управления задачами и анализа загруженности сотрудников.

## Стек
- Python 3.11, Django 4.2, Django REST Framework
- PostgreSQL 16
- Docker Compose
- pytest + pytest-django (тесты), flake8 (линт), drf-spectacular (Swagger)

## Запуск
    docker compose up --build -d
    docker compose exec web python manage.py migrate
    docker compose exec web python manage.py createsuperuser

## Эндпоинты
- Swagger: http://localhost:8000/api/docs/
- CRUD сотрудников: /api/employees/
- CRUD задач: /api/tasks/
- Сводка загруженности: /api/employees/workload/
- Разбивка по статусам: /api/employees/{id}/detail_workload/
- Подбор исполнителя: /api/tasks/{id}/suggest_assignee/

## Тесты
    docker compose exec web pytest -v
