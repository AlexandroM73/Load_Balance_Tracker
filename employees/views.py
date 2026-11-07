from django.db.models import Count, Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filterset_fields = ["position", "is_active"]
    search_fields = ["full_name", "email"]

    @action(detail=False, methods=["get"])
    def workload(self, request):
        """Сводка загруженности по всем активным сотрудникам."""
        employees = (
            Employee.objects.filter(is_active=True)
            .annotate(
                open_tasks=Count(
                    "tasks",
                    filter=~Q(tasks__status="done"),
                )
            )
            .order_by("open_tasks")
        )
        return Response(
            [
                {
                    "id": e.id,
                    "full_name": e.full_name,
                    "position": e.position,
                    "open_tasks": e.open_tasks,
                }
                for e in employees
            ]
        )

    @action(detail=True, methods=["get"])
    def detail_workload(self, request, pk=None):
        """Загруженность одного сотрудника с разбивкой по статусам."""
        employee = self.get_object()
        stats = dict(
            employee.tasks.exclude(status="done")
            .values_list("status")
            .annotate(cnt=Count("id"))
        )
        return Response(
            {
                "id": employee.id,
                "full_name": employee.full_name,
                "open_tasks": sum(stats.values()),
                "by_status": stats,
            }
        )
