import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.models import ProtectedError

from apps.occurrences.models import Occurrence
from apps.guards.models import Guard


def sample_user():
    return get_user_model().objects.create_user(
        email='user@email.com',
        password='hispass'
    )


def sample_guard():
    return Guard.objects.create(
        cod_guard='12314123',
        name='guard name'
    )


def sample_occurrence(user, guard, created_at=datetime.date.today(), _status=0):
    return Occurrence.objects.create(
        user=user,
        guard=guard,
        license_plate='abc0000',
        occurrence_type='Batida',
        occurrence_title='Me bateram aqui aaa',
        location='Rua 2 do bairro 1',
        status=_status,
        created_at=created_at
    )


class OccurrenceModelTests(TestCase):
    def setUp(self):
        self.user = sample_user()
        self.guard = sample_guard()
        self.occurrence = sample_occurrence(self.user, self.guard)

    def test_str_representation_order(self):
        occurrence_str = self.occurrence.occurrence_title

        self.assertEqual(str(self.occurrence), str(occurrence_str),
                         'str of occurrence must be its title')

    def test_delete_user_protect(self):
        """Test deletion of user protect deletion of occurrence"""
        self.assertRaises(ProtectedError, self.user.delete)

    def test_delete_guard_protect(self):
        """Test deletion of user protect deletion of occurrence"""
        self.assertRaises(ProtectedError, self.guard.delete)

    def test_default_occurrence_params(self):
        self.assertEqual(self.occurrence.created_at, datetime.date.today(),
                         'for default created_at of occurrence must be the day of creation)')
        self.assertEqual(self.occurrence.status, 0,
                         'when created occurrence.status must be 0 ("aguardando envio de boleto")')

    def test_order_of_model_queryset(self):
        """Test if the order of Occurrence"""
        Occurrence.objects.all().delete()
        occurrences = []
        for day in range(10, 1, -1):
            created_at = datetime.date.today() + datetime.timedelta(day)
            occurrences.append(sample_occurrence(self.user, self.guard, created_at=created_at))

        self.assertEqual(occurrences, [*Occurrence.objects.all()],
                         'Occurrence must be retrieved by newest to oldest')
