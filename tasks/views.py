from django.db.models import Count, Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from employees.models import Employee
from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related("assignee", "parent")
    serializer_class = TaskSerializer
    filterset_fields = ["status", "assignee"]
    search_fields = ["title", "description"]

    @action(detail=True, methods=["get"])
    def suggest_assignee(self, request, pk=None):
        """Подбор исполнителя: активный сотрудник с минимальным числом незавершённых задач."""
        task = self.get_object()

        candidates = (
            Employee.objects.filter(is_active=True)
            .annotate(
                open_tasks=Count(
                    "tasks",
                    filter=~Q(tasks__status=Task.Status.DONE),
                )
            )
            .order_by("open_tasks", "id")
        )

        if not candidates:
            return Response(
                {"detail": "Нет активных сотрудников"},
                status=status.HTTP_404_NOT_FOUND,
            )

        best = candidates.first()
        return Response(
            {
                "task": task.title,
                "suggested_assignee_id": best.id,
                "suggested_assignee": best.full_name,
                "their_open_tasks": best.open_tasks,
            }
        )
