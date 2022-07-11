from django.db import models
from django.contrib.postgres import fields as psql_fields
from django.core.exceptions import ObjectDoesNotExist

from django.utils import timezone


class ResumeSource(models.Model):
    name = models.CharField(max_length=100)


class Citizenship(models.Model):
    name = models.CharField(max_length=30)


class ContactType(models.Model):
    name = models.CharField(max_length=30)


class Candidate(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField()
    position = models.CharField(max_length=100)
    citizenship = models.ForeignKey(Citizenship, on_delete=models.RESTRICT)
    salary = models.CharField(max_length=50)
    contacts = models.ManyToManyField('ContactType', through='Contact')


class Contact(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.RESTRICT)
    contact_type = models.ForeignKey(ContactType, on_delete=models.RESTRICT)
    value = models.CharField(max_length=50)


class Document(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.RESTRICT)
    document = models.FileField()


class Resume(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.RESTRICT)
    source = models.ForeignKey(ResumeSource, on_delete=models.RESTRICT)
    link = models.URLField(null=True, blank=True)
    update_date = models.DateTimeField()
    position = models.CharField(max_length=100)
    experience = models.PositiveSmallIntegerField()
    skills = psql_fields.ArrayField(base_field=models.CharField(max_length=100))
    salary = models.CharField(max_length=50)
    detailed_experience = models.TextField()  # TODO: improve this field
    about = models.TextField()

    NEW = 10
    PHONE_INTERVIEW = 20
    SCHEDULED_RECRUIT_INTERVIEW = 30
    PRIMARY_RECRUIT_INTERVIEW = 40
    RESUME_AT_CUSTOMER = 50
    TEST_JOB = 60
    SCHEDULED_CUSTOMER_INTERVIEW = 70
    DEV_TEST = 1000

    PHASE_CHOICES = [
        (NEW, 'Новый сотрудник'),
        (PHONE_INTERVIEW, 'Телефонное интервью'),
        (SCHEDULED_RECRUIT_INTERVIEW, 'Назначено интервью с рекрутом'),
        (PRIMARY_RECRUIT_INTERVIEW, 'Первичное интервью с рекрутом'),
        (RESUME_AT_CUSTOMER, 'Резюме у заказчика'),
        (TEST_JOB, 'Тестовое задание'),
        (SCHEDULED_CUSTOMER_INTERVIEW, 'Назначено интервью с заказчиком'),
        (DEV_TEST, 'ТЕСТ'),
    ]
    phase = models.PositiveSmallIntegerField(choices=PHASE_CHOICES, default=PHASE_CHOICES[0][0])


class Department(models.Model):
    name = models.CharField(max_length=50)


class Vacancy(models.Model):
    name = models.CharField(max_length=100)
    is_open = models.BooleanField(default=True)

    NEW = 0
    REPLACE = 1
    STATUS_CHOICES = [
        (NEW, 'Новый сотрудник'),
        (REPLACE, 'Замена'),
    ]
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])

    skills = psql_fields.ArrayField(base_field=models.CharField(max_length=100))
    location = models.CharField(max_length=250, default='Кировская область, г. Киров')
    department = models.ForeignKey(Department, on_delete=models.RESTRICT)
    project = models.CharField(max_length=100)
    salary = models.CharField(max_length=50)

    resumes = models.ManyToManyField(Resume)


def add_candidate(**kwargs):

    new_candidate = Candidate.objects.create(
        name=kwargs.get('name'),
        age=kwargs.get('age'),
        position=kwargs.get('position'),
        citizenship=Citizenship.objects.get_or_create(name=kwargs.get('citizenship'))[0],
        salary=kwargs.get('position')
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
    try:
        kwargs['candidate'] = Candidate.objects.get(pk=kwargs['candidate_id'])
    except ObjectDoesNotExist:
        return False
    else:
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


def contacts_dicts(candidate_pk):
    """
    Build list of {contact_type: contact_value} dicts of specific Candidate by his ID
    """
    contacts = Contact.objects.filter(candidate=candidate_pk)
    contact_list = [{contact.contact_type.name: contact.value} for contact in contacts]
    return contact_list



