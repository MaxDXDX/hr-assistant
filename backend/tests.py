# import datetime as dt
from django.utils import timezone
import pytz

from django.test import TestCase
from backend.models import *


class DBCreateTestCase(TestCase):
    def setUp(self):
        # filling primary tables
        Department.objects.bulk_create(
            [
                Department(name='1C'),
                Department(name='Web'),
            ]
        )

        Citizenship.objects.bulk_create(
            [
                Citizenship(name='Россия'),
                Citizenship(name='Беларусь'),
                Citizenship(name='Казахстан'),
            ]
        )

        ContactType.objects.bulk_create(
            [
                ContactType(name='Phone'),
                ContactType(name='E-mail'),
                ContactType(name='VK'),
                ContactType(name='Telegram'),
            ]
        )

        ResumeSource.objects.bulk_create(
            [
                ResumeSource(name='hh.ru'),
                ResumeSource(name='e-mail'),
                ResumeSource(name='лично'),
                ResumeSource(name='github'),
                ResumeSource(name='geekjob'),
                ResumeSource(name='joblab'),
            ]
        )

        # creating two vacancies
        vacancy_1 = Vacancy(
            name='Junior Frontend разработчик',
            is_open=True,
            status=Vacancy.NEW,
            skills=[
                'Знание и опыт программирования на Javascript/CSS/HTML',
                'Нативный Javascript без jQuery',
                'Представление о mobile-friendly фронтенде',
            ],
            location='г. Ижевск',
            department=Department.objects.get(name='Web'),
            project='Первое веб-приложение',
            salary='50000 - 80000 руб.',
        )
        vacancy_1.save()

        vacancy_2 = Vacancy(
            name='Middle 1C разработчик',
            is_open=True,
            status=Vacancy.REPLACE,
            skills=[
                'Кодить на платформе 8.3 (управляемые формы, СКД)',
                'Знание основных механизмов 1С',
                'Сертификат 1С приветствуется',
            ],
            location='г. Киров',
            department=Department.objects.get(name='1C'),
            project='Мощный проект',
            salary='100000 - 150000 руб.',
        )
        vacancy_2.save()

        # creating 1/2 candidate with two resumes
        candidate_1 = Candidate.objects.create(
            name='Иванов Иван',
            age=35,
            position='Frontend разработчик',
            citizenship=Citizenship.objects.get(name='Россия'),
            salary='от 50000 руб.'
        )
        candidate_1.save()
        Contact.objects.bulk_create(
            [
                Contact(
                    candidate=candidate_1,
                    contact_type=ContactType.objects.get(name='Phone'),
                    value='+71111111111'
                ),
                Contact(
                    candidate=candidate_1,
                    contact_type=ContactType.objects.get(name='E-mail'),
                    value='1111@mail.11'
                ),
                Contact(
                    candidate=candidate_1,
                    contact_type=ContactType.objects.get(name='VK'),
                    value='vk.com/id1111111'
                ),
            ]
        )

        # creating 1/2 resume of 1/2 candidate
        candidate_1_resume_1 = Resume(
            candidate=candidate_1,
            source=ResumeSource.objects.get(name='hh.ru'),
            link='https://kirov.hh.ru/resume/11111111111111111111111111111111111111',
            # update_date=dt.datetime.now(),
            update_date=timezone.now(),
            position='Full-stack разработчик',
            experience=2,
            skills=[
                'уверенное знание HTML/CSS/JS',
                'опыт коммерческой разработки',
                'разработка приложений на ReactJS',
                'опыт работы в мобильной разработке',
            ],
            salary='от 1000 $',
            detailed_experience='2010-2012: Компания-1\nДолжность\n-обязанность1\nОбязанность2\n',
            about='Я очень очень хороший разработчик',
            phase=Resume.PHASE_CHOICES[0][0],
        )
        candidate_1_resume_1.save()

        # creating 2/2 resume of 1/2 candidate
        candidate_1_resume_2 = Resume(
            candidate=candidate_1,
            source=ResumeSource.objects.get(name='e-mail'),
            link=None,
            # update_date=dt.datetime.now(),
            update_date=timezone.now(),
            position='1С разработчик',
            experience=4,
            skills=[
                'могу кодить на 1С',
                'а могу и не кодить на 1С',
                'но лучше кодить, чем не кодить на 1С',
            ],
            salary='от 500 Евро',
            detailed_experience='2020-2021: Компания-1\nДолжность\n-обязанность1\nОбязанность2\n',
            about='Я универсальный разработчик',
            phase=Resume.PHASE_CHOICES[5][0],
        )
        candidate_1_resume_2.save()

        # creating 2/2 candidate with 2 resumes
        candidate_2 = Candidate.objects.create(
            name='Петр Петров',
            age=35,
            position='Fullstack разработчик',
            citizenship=Citizenship.objects.get(name='Беларусь'),
            salary='от 50000 руб.'
        )
        candidate_2.save()
        Contact.objects.bulk_create(
            [
                Contact(
                    candidate=candidate_2,
                    contact_type=ContactType.objects.get(name='Phone'),
                    value='+72222222222'
                ),
                Contact(
                    candidate=candidate_2,
                    contact_type=ContactType.objects.get(name='E-mail'),
                    value='2222@mail.22'
                ),
                Contact(
                    candidate=candidate_2,
                    contact_type=ContactType.objects.get(name='Telegram'),
                    value='@2222'
                ),
            ]
        )

        # creating 1/2 resume of 2/2 candidate
        candidate_2_resume_1 = Resume(
            candidate=candidate_2,
            source=ResumeSource.objects.get(name='geekjob'),
            link='https://geekjob.ru/geek/222222222222222222222222222222',
            # update_date=dt.datetime.now(),
            update_date=timezone.now(),
            position='Full-stack разработчик',
            experience=6,
            skills=[
                'навык 1/4 резюме 1/2 кандидата 2/2',
                'навык 2/4 резюме 1/2 кандидата 2/2',
                'навык 3/4 резюме 1/2 кандидата 2/2',
                'навык 4/4 резюме 1/2 кандидата 2/2',
            ],
            salary='от 2000 Евро',
            detailed_experience='2016-2022: Компания-2\nДолжность\n-обязанность1\nОбязанность2\n',
            about='Я кандидат 2/2 и это моё 1/2 резюме',
            phase=Resume.PHASE_CHOICES[0][0],
        )
        candidate_2_resume_1.save()

        # creating 2/2 resume of 2/2 candidate
        candidate_2_resume_2 = Resume(
            candidate=candidate_2,
            source=ResumeSource.objects.get(name='e-mail'),
            link=None,
            # update_date=dt.datetime.now(),
            update_date=timezone.now(),
            position='Senior 1С разработчик',
            experience=14,
            skills=[
                'навык 1/4 резюме 2/2 кандидата 2/2',
                'навык 2/4 резюме 2/2 кандидата 2/2',
                'навык 3/4 резюме 2/2 кандидата 2/2',
                'навык 4/4 резюме 2/2 кандидата 2/2',
            ],
            salary='от 1 биткоина',
            detailed_experience='2007-2021: Компания-1\nДолжность\n-обязанность1\nОбязанность2\n',
            about='Я кандидат 2 и это моё второе резюме',
            phase=Resume.PHASE_CHOICES[5][0],
        )
        candidate_2_resume_2.save()

        # adding resume(s) to vacancy(ies)
        vacancy_1.resumes.add(candidate_1_resume_1)
        vacancy_1.resumes.add(candidate_2_resume_1)
        vacancy_2.resumes.add(candidate_1_resume_2)
        vacancy_2.resumes.add(candidate_2_resume_2)

    def test_vacancy_count(self):
        """Get resume count of vacancy"""
        vacancy = Vacancy.objects.all()
        self.assertEqual(len(vacancy), 2)

    def test_contact(self):
        """Get one contact"""
        candidate = Candidate.objects.get(name='Иванов Иван')
        contact_list = Contact.objects.filter(candidate=candidate)

        contacts = [(contact.contact_type.name, contact.value) for contact in contact_list]

        candidate_1_contacts = (
            [
                ('Phone', '+71111111111'),
                ('E-mail', '1111@mail.11'),
                ('VK', 'vk.com/id1111111')
            ]
        )

        self.assertEqual(contacts, candidate_1_contacts)



