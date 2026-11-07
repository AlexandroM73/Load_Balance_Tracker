from django.db import models


class Employee(models.Model):
    full_name = models.CharField("ФИО", max_length=255)
    position = models.CharField("Должность", max_length=100)
    email = models.EmailField("Email", unique=True)
    is_active = models.BooleanField("Активен", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["full_name"]
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return f"{self.full_name} ({self.position})"
