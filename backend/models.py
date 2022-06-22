from django.db import models
from django.contrib.postgres import fields as psql_fields


class Department(models.Model):
    name = models.TextField()


class Vacancy(models.Model):
    name = models.TextField()
    is_open = models.BooleanField(default=True)

    NEW = 'new'
    REPLACE = 'replace'
    STATUS_CHOICES = [
        (NEW, 'Новый сотрудник'),
        (REPLACE, 'Замена'),
    ]
    status = models.TextField(choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])

    skills = psql_fields.ArrayField(base_field=models.TextField())
    location = models.TextField(default='Кировская область, г. Киров')
    department = models.ForeignKey(Department, on_delete=models.RESTRICT)
    project = models.TextField()
    salary = models.TextField()
