from backend.models import *
from backend.serializer import HrSerializer


def handler(method, params):

    # TODO: add filters
    if method == 'get-all-vacancies':
        s = HrSerializer(Vacancy, array_fields=['skills'])
        data = s.correct_items()

    elif method == 'get-all-candidates':
        s = HrSerializer(Candidate)
        data = s.correct_items()

    elif method == 'get-all-resumes':
        s = HrSerializer(Resume, array_fields=['skills'])
        data = s.correct_items()

    # TODO: return added item in response on 'add-*' methods

    elif method == 'add-vacancy':
        add_vacancy(**params)
        data = 'Вакансия добавлена'

    elif method == 'add-candidate':
        add_candidate(**params)
        data = 'Кандидат добавлен'

    elif method == 'add-resume':
        add_resume(**params)
        data = 'Резюме добавлено'
    else:
        data = dict(error='Unknown Method')

    return data
