import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model

from apps.occurrences.models import Occurrence
from apps.guards.models import Guard


def sample_user():
    return get_user_model.objects.create_user(
        email='user@email.com',
        password='hispass'
    )

def sample_guard():
    return Guard.objects.create(
        cod_guard='12314123',
        name='guard name'
    )

def sample_occurrence(user, guard):
    return Occurrence.objects.create(
        user=user,
        license_plate='abc0000',
        occurrence_type='Batida',
        occurence_title='Me bateram aqui aaa',
        location='Rua 2 do bairro 1',
        date=datetime.date.today(),
        guard=guard
    )


class OccurrenceModelTests(TestCase):
    def setUp(self):
        self.user = sample_user()
        self.guard = sample_guard()
        self.occurrence = sample_occurrence(self.user,sample_guard)

    

