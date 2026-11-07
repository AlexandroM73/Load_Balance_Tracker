from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    assignee_name = serializers.CharField(source="assignee.full_name", read_only=True)

    class Meta:
        model = Task
        fields = [
            "id", "title", "parent", "assignee", "assignee_name",
            "due_date", "status", "description", "created_at",
        ]
        read_only_fields = ["id", "created_at", "assignee_name"]

    def validate_assignee(self, value):
        if value is not None and not value.is_active:
            raise serializers.ValidationError(
                "Нельзя назначить задачу неактивному сотруднику."
            )
        return value

    def validate_due_date(self, value):
        from django.utils import timezone
        if value < timezone.localdate():
            raise serializers.ValidationError("Срок не может быть в прошлом.")
        return value
