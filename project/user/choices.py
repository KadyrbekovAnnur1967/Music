from django.db import models

class RoleChoices(models.TextChoices):
    ADMINISTRATOR = ('administrator', 'Администратор')
    REDACTOR = ('redactor', 'Редактор')
    LISTENER = ('listener', 'Слушатель')