from django.db import models
from django.contrib.postgres import fields as psql_fields

from django.utils import timezone


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
        (1000, 'ТЕСТ'),
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


def add_candidate(**kwargs):

    new_candidate = Candidate.objects.create(
        name=kwargs['name'],
        age=kwargs['age'],
        position=kwargs['position'],
        citizenship=Citizenship.objects.get_or_create(name=kwargs['citizenship'])[0],
        salary=kwargs['position']
    )

    for contact in kwargs['contacts']:
        Contact.objects.create(
            candidate=new_candidate,
            contact_type=ContactType.objects.get_or_create(name=contact['type'])[0],
            value=contact['value']
        )


def add_vacancy(**kwargs):
    kwargs['department'] = Department.objects.get_or_create(name=kwargs['department'])[0]
    new_vacancy = Vacancy(**kwargs)
    new_vacancy.save()


def add_resume(**kwargs):
    kwargs['candidate'] = Candidate.objects.get(pk=kwargs['candidate_id'])
    kwargs['source'] = ResumeSource.objects.get_or_create(name=kwargs['candidate'])[0]
    kwargs['update_date'] = timezone.now()
    if 'vacancy_ids' in kwargs:
        vacancy_ids = kwargs.pop('vacancy_ids')
    else:
        vacancy_ids = None

    new_resume = Resume(**kwargs)
    new_resume.save()

    if vacancy_ids:
        for vacancy_id in vacancy_ids:
            Vacancy.objects.get(pk=vacancy_id).resumes.add(new_resume)



def set_resume_phase(resume_id, phase_id):
    resume = Resume.objects.get(pk=resume_id)
    resume.phase = phase_id
    resume.save()


def update_record(model, data):
    row_id = data.pop('id')
    if model == 'candidate':
        candidate = Candidate.objects.filter(id=row_id)

        if 'citizenship' in data:
            new_citizenship = data.pop('citizenship')
            data['citizenship'] = Citizenship.objects.get_or_create(name=new_citizenship)[0].id

        if 'contacts' in data:
            # remove old contacts
            Contact.objects.filter(candidate=candidate[0]).delete()

            new_contacts = data.pop('contacts')
            for contact in new_contacts:
                Contact.objects.create(
                    candidate=candidate[0],
                    contact_type=ContactType.objects.get_or_create(name=contact)[0],
                    value=new_contacts[contact]
                )

        candidate.update(**data)

    elif model == 'resume':
        resume = Resume.objects.filter(id=row_id)
        if 'source' in data:
            new_source = data.pop('source')
            data['source'] = ResumeSource.objects.get_or_create(name=new_source)[0].id
        resume.update(**data)

    elif model == 'vacancy':
        vacancy = Vacancy.objects.filter(id=row_id)
        if 'department' in data:
            new = data.pop('department')
            data['department'] = Department.objects.get_or_create(name=new)[0].id
        vacancy[0].update_date = timezone.now()
        vacancy.update(**data)

def vacancy_resumes(vacancy_id, resume_ids: list):
    for resume_id in resume_ids:
        vacancy = Vacancy.objects.get(pk=vacancy_id)
        vacancy.resumes.add(resume_id)





