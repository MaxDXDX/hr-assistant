import json

from django.core.serializers import serialize
from backend.models import *


class HrSerializer:
    """Custom serializer to add some bonus features to standard Django serializer"""

    def __init__(self, model, array_fields=None):
        self.model = model
        self.objects = model.objects.all()
        self.default = json.loads(serialize('json', self.objects))
        self.array_fields = array_fields

    def rebuild_item_array_fields(self, item, item_index):
        """Replace incorrect serialized list object by custom method"""
        if self.array_fields:
            for field in self.array_fields:
                array_items = getattr(self.objects[item_index], field)
                item['fields'][field] = array_items

    def correct_items(self):
        """Iterate all items and add some features to each"""
        result = self.default.copy()

        for index, item in enumerate(self.default):
            pk = item['pk']

            # rebuild arrayFields (for all models)
            self.rebuild_item_array_fields(item, index)

            if self.model == Candidate:
                candidate = self.objects.get(pk=pk)

                # add pretty styled contacts to Candidate from m2m field
                item['fields']['contacts'] = contacts_dicts(pk)

                # add ids of all candidate resumes
                item['resume_ids'] = [resume.pk for resume in candidate.resume_set.all()]

            if self.model == Vacancy:
                vacancy = self.objects.get(pk=pk)

                # add pretty styled contacts to Candidate from m2m field
                item['fields']['contacts'] = contacts_dicts(pk)

            if self.model == Resume:
                resume = self.objects.get(pk=pk)

                # add ids of all vacancies which gotten this resume
                item['fields']['vacancy_ids'] = [vacancy.pk for vacancy in resume.vacancy_set.all()]

        return result




