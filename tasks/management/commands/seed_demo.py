from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from employees.models import Employee
from tasks.models import Task


class Command(BaseCommand):
    help = "Наполняет базу демо-данными (сотрудники и задачи)."

    def handle(self, *args, **options):
        next_week = timezone.localdate() + timedelta(days=7)

        employees_data = [
            ("Иванов Иван Иванович", "Разработчик", "ivanov@example.com"),
            ("Петрова Анна Сергеевна", "Аналитик", "petrova@example.com"),
            ("Сидоров Пётр Николаевич", "Тестировщик", "sidorov@example.com"),
            ("Козлова Мария Викторовна", "Разработчик", "kozlova@example.com"),
        ]

        employees = []
        for full_name, position, email in employees_data:
            emp, _ = Employee.objects.get_or_create(
                email=email,
                defaults={"full_name": full_name, "position": position},
            )
            employees.append(emp)

        tasks_data = [
            ("Спроектировать схему БД", None, employees[1], "done", "ER-диаграмма и миграции"),
            ("Реализовать API сотрудников", None, employees[0], "in_progress", "CRUD + валидация"),
            ("Написать тесты для задач", None, employees[2], "in_progress", "pytest, позитивные и негативные кейсы"),
            ("Подготовить документацию", None, employees[3], "new", "Swagger и README"),
            ("Настроить CI", None, employees[0], "new", "lint и автотесты на каждый пуш"),
            ("Провести ревью кода", None, employees[3], "done", "Проверка замечаний линтера"),
        ]

        created = 0
        for title, parent, assignee, status, description in tasks_data:
            _, was_created = Task.objects.get_or_create(
                title=title,
                defaults={
                    "parent": parent,
                    "assignee": assignee,
                    "due_date": next_week,
                    "status": status,
                    "description": description,
                },
            )
            created += int(was_created)

        self.stdout.write(
            self.style.SUCCESS(f"Готово: {len(employees)} сотрудников, создано новых задач: {created}")
        )
