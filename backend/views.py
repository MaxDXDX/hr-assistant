
import json
import pprint

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from backend.models import *

from django.core.serializers import serialize




class HomePageView(TemplateView):
    template_name = 'home.html'

@csrf_exempt
def api(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        method = body.get('method')
        r_id = body.get('id')

        if method == 'get-all-vacancies':
            vacancies = Vacancy.objects.all()

            # exluded_fields = ['skills']
            # fields = tuple([field.name for field in Vacancy._meta.get_fields() if field.name not in exluded_fields])
            # data = serialize('json', vacancies, fields=fields)

            data = serialize('json', vacancies)
            data_dic = json.loads(data)
            for item in data_dic:
                incorrect = item['fields']['skills']
                correct = bytes(incorrect, "ascii").decode("unicode-escape")
                item['fields']['skills'] = correct
            data = json.dumps(data_dic, ensure_ascii=False)
            data = data.replace('"[', '[').replace(']"', ']').replace('\\', '')

        elif method == 'get-all-candidates':
            candidates = Candidate.objects.all()
            data = serialize('json', candidates)
            data_dic = json.loads(data)
            for item in data_dic:
                candidate_pk = item.get('pk')
                # candidate = Candidate.objects.get(pk=candidate_pk)

                contacts = Contact.objects.filter(candidate=candidate_pk)
                contact_list = [{contact.contact_type.name: contact.value}  for contact in contacts]
                item['fields']['contacts'] = contact_list

                resumes = Candidate.objects.get(pk=candidate_pk).resume_set.all()
                resume_list = [resume.pk for resume in resumes]
                item['fields']['resumes'] = resume_list

            data = json.dumps(data_dic, ensure_ascii=False)

        elif method == 'get-all-resumes':
            resumes = Resume.objects.all()
            data = serialize('json', resumes)
            data_dic = json.loads(data)
            for item in data_dic:
                item_id = item.get('pk')
                incorrect = item['fields']['skills']
                correct = bytes(incorrect, "ascii").decode("unicode-escape")
                item['fields']['skills'] = correct
                vacancies = Resume.objects.get(pk=item_id).vacancy_set.all()
                vacancy_list = [vacancy.pk for vacancy in vacancies]
                item['fields']['vacancies'] = vacancy_list

            data = json.dumps(data_dic, ensure_ascii=False)
            data = data.replace('"[', '[').replace(']"', ']').replace('\\', '')

        elif method == 'add-vacancy':
            print('Creating new vacancy...')
            params = body.get('params')
            add_vacancy(**params)
            data = 'Вакансия добавлена'

        elif method == 'add-candidate':
            print('Creating new candidate...')
            params = body.get('params')
            add_candidate(**params)
            data = 'Кандидат добавлен'

        elif method == 'add-resume':
            print('Creating new resume...')
            params = body.get('params')
            add_resume(**params)
            data = 'Резюме добавлено'
        else:
            data = dict(error='Unknown Method')
    else:
        data = {'error': 'use POST method'}
    # return JsonResponse(data, safe=False)
    return HttpResponse(data)

