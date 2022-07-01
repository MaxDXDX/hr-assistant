from django.db import models
from django.contrib.postgres import fields as psql_fields


class ResumeSource(models.Model):
    name = models.TextField()


class Citizenship(models.Model):
    name = models.TextField()


class ContactType(models.Model):
    name = models.TextField()


class Candidate(models.Model):
    name = models.TextField()
    age = models.PositiveSmallIntegerField()
    position = models.TextField()
    citizenship = models.ForeignKey(Citizenship, on_delete=models.RESTRICT)
    salary = models.TextField()
    contacts = models.ManyToManyField('ContactType', through='Contact')


class Contact(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.RESTRICT)
    contact_type = models.ForeignKey(ContactType, on_delete=models.RESTRICT)
    value = models.TextField()


class Document(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.RESTRICT)
    document = models.FileField()


class Resume(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.RESTRICT)
    source = models.ForeignKey(ResumeSource, on_delete=models.RESTRICT)
    link = models.URLField(null=True, blank=True)
    update_date = models.DateTimeField()
    position = models.TextField()
    experience = models.PositiveSmallIntegerField()
    skills = psql_fields.ArrayField(base_field=models.TextField())
    salary = models.TextField()
    detailed_experience = models.TextField()  # TODO: to improve this field
    about = models.TextField()

    PHASE_CHOICES = [
        (0, 'Новый сотрудник'),
        (1, 'Телефонное интервью'),
        (2, 'Назначено интервью с рекрутом'),
        (3, 'Первичное интервью с рекрутом'),
        (4, 'Резюме у заказчика'),
        (5, 'Тестовое задание'),
        (6, 'Назначено интервью с заказчиком'),
    ]
    phase = models.PositiveSmallIntegerField(choices=PHASE_CHOICES, default=PHASE_CHOICES[0][0])


class Department(models.Model):
    name = models.TextField()


class Vacancy(models.Model):
    name = models.TextField()
    is_open = models.BooleanField(default=True)

    NEW = 0
    REPLACE = 1
    STATUS_CHOICES = [
        (NEW, 'Новый сотрудник'),
        (REPLACE, 'Замена'),
    ]
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])

    skills = psql_fields.ArrayField(base_field=models.TextField())
    location = models.TextField(default='Кировская область, г. Киров')
    department = models.ForeignKey(Department, on_delete=models.RESTRICT)
    project = models.TextField()
    salary = models.TextField()

    resumes = models.ManyToManyField(Resume)

