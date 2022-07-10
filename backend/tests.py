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
            name='Кандидат Первый',
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
            name='Кандидат Второй',
            age=35,
            position='Fullstack разработчик',
            citizenship=Citizenship.objects.get(name='Беларусь'),
            salary='от 50000 руб.'
        )
        # candidate_2.save()
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

    def test_get_contact(self):
        """Get candidate contacts"""
        candidate = Candidate.objects.get(name='Кандидат Первый')
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

    def test_add_new_contact_with_new_type(self):
        """Add new contact of new type"""
        candidate_name = 'Кандидат Второй'
        candidate = Candidate.objects.get(name=candidate_name)
        previous_contacts = [
            (contact.contact_type.name, contact.value) for contact in Contact.objects.filter(candidate=candidate)
        ]

        new_contact = {
            'type': 'testogram',
            'value': '@testogram-account'
        }

        contact_type, created = ContactType.objects.get_or_create(name=new_contact['type'])

        Contact.objects.create(
            candidate=candidate,
            contact_type=contact_type,
            value=new_contact['value']
        )

        assert_contacts = [
            ('Phone', '+72222222222'),
            ('E-mail', '2222@mail.22'),
            ('Telegram', '@2222'),
            (new_contact['type'], new_contact['value'])
        ]

        updated_contacts = [
            (contact.contact_type.name, contact.value) for contact in Contact.objects.filter(candidate=candidate)
        ]

        self.assertEqual(assert_contacts, updated_contacts)

    def test_add_candidate(self, **kwargs):
        error = False
        try:
            add_candidate(
                name='Новый кандидат',
                age=67,
                position='Должность нового кандидата',
                citizenship='Страна нового кандидата',
                salary='Ожидаемый оклад нового кандидата',
                contacts=[
                    {'type': 'Phone', 'value': '+7123456789'},
                    {'type': 'E-mail', 'value': 'new_cand@new_cand.ru'},
                    {'type': 'Новый вид связи', 'value': 'значение нового вида связи'},
                ]
            )
        except ValueError:
            error = True

        self.assertFalse(error)

    def test_add_vacancy(self, **kwargs):
        error = False
        try:
            add_vacancy(
                name='Новая вакансия',
                is_open=True,
                status=Vacancy.NEW,
                skills=[
                    'Навык 1 для новой вакансии',
                    'Навык 2 для новой вакансии',
                    'Навык 3 для новой вакансии',
                ],
                location='местоположение новой вакансии',
                department='1С',
                project='Проект новой вакансии',
                salary='Оклад новой вакансии',
            )
        except ValueError:
            error = True

        self.assertFalse(error)

    def test_add_resume(self, **kwargs):
        error = False
        try:
            add_resume(
                candidate_id=Candidate.objects.first().pk,
                source='Источник нового резюме',
                link='https:/hh.ru/resume',
                # update_date=None,
                position='Желаемая должность',
                experience=3,
                skills=[
                    'Навык 1 в резюме',
                    'Навык 2 в резюме',
                    'Навык 3 в резюме',
                ],
                salary='Желаемый оклад',
                detailed_experience="""2020-2022: Компания 1 - Должность 1
                2018-2020: Компания 2 - Должность 2
                2016-2018: Компания 3 - Должность 3
                """,
                about='Информация о себе',
                phase=5,
                vacancy_ids=[Vacancy.objects.all()[0].id, Vacancy.objects.all()[1].id]
            )
        except ValueError:
            error = True

        self.assertFalse(error)

    def test_set_resume_phase(self):
        """Set resume phase by its ID"""
        some_resume_id = Resume.objects.first().pk
        set_resume_phase(some_resume_id, 1000)

        updated_resume = Resume.objects.get(pk=some_resume_id)
        self.assertEqual(1000, updated_resume.phase)

    def test_update_candidate(self):
        """Update candidate data"""
        row_id = Candidate.objects.get(name='Кандидат Первый').id
        new_data = {
            'name': 'Обновленное имя',
            'age': 99,
            'position': 'Обновленная должность',
            'citizenship': 'Обновленное гражданство',
            'salary': 'Обновленный оклад',
            'contacts': {
                'Новый вид связи #1': 'Значение для нового вида связи #1',
                'Новый вид связи #2': 'Значение для нового вида связи #2',
                'Новый вид связи #3': 'Значение для нового вида связи #3',
            }
        }

        data = new_data.copy()
        data['id'] = row_id

        update_record('candidate', data)

        updated_candidate = Candidate.objects.get(id=row_id)
        # print('sch: ', updated_candidate.citizenship)
        # print('sch: ', Citizenship.objects.get(updated_candidate.citizenship).name)

        updated_contacts = {
            contact.contact_type.name: contact.value
            for contact in Contact.objects.filter(candidate=row_id)
        }

        updated_data = {
            'name': updated_candidate.name,
            'age': updated_candidate.age,
            'position': updated_candidate.position,
            'citizenship': updated_candidate.citizenship.name,
            'salary': updated_candidate.salary,
            'contacts': updated_contacts,
        }
        self.assertEqual(new_data, updated_data)

    def test_update_resume(self):
        """Update resume data"""
        row_id = Resume.objects.first().id
        new_data = {
            'source': 'Обновленный источник',
            'link': 'Обновленная ссылка',
            # 'update_date': 'Обновленная дата обновления',
            'position': 'Обновленная желаемая должность',
            'experience': 99,
            'skills': [
                'Обновленный навык #1',
                'Обновленный навык #2',
                'Обновленный навык #3',
            ],
            'salary': 'Обновленный ожидаемый оклад',
            'detailed_experience': 'Обновленный детальный опыт работы',
            'about': 'Обновленное <о себе>',
            'phase': 1000,
        }

        data = new_data.copy()
        data['id'] = row_id

        update_record('resume', data)
        updated_record = Resume.objects.get(id=row_id)

        updated_data = {
            'source': updated_record.source.name,
            'link': updated_record.link,
            # 'update_date': 'Обновленная дата обновления',
            'position': updated_record.position,
            'experience': updated_record.experience,
            'skills': updated_record.skills,
            'salary': updated_record.salary,
            'detailed_experience': updated_record.detailed_experience,
            'about': updated_record.about,
            'phase': updated_record.phase,
        }
        self.assertEqual(new_data, updated_data)

    def test_update_vacancy(self):
        """Update vacancy data"""
        row_id = Vacancy.objects.first().id
        new_data = {
            'name': 'Обновленное наименование вакансии',
            'is_open': False,
            # 'update_date': 'Обновленная дата обновления',
            'status': Vacancy.REPLACE,
            'skills': [
                'Обновленный навык #1 для вакансии',
                'Обновленный навык #2 для вакансии',
                'Обновленный навык #3 для вакансии',
            ],
            'location': 'Обновленное местоположении вакансии',
            'department': 'Обновленный отдел',
            'project': 'Обновленный проект',
            'salary': 'Обновленный оклад',
        }

        data = new_data.copy()
        data['id'] = row_id

        update_record('vacancy', data)
        updated_record = Vacancy.objects.get(id=row_id)

        updated_data = {
            'name': updated_record.name,
            'is_open': updated_record.is_open,
            'status': updated_record.status,
            'skills': updated_record.skills,
            'location': updated_record.location,
            'department': updated_record.department.name,
            'project': updated_record.project,
            'salary': updated_record.salary,
        }
        self.assertEqual(new_data, updated_data)


