from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..api.serializers import OccurrenceSerializer
from ..models import Occurrence
from ...guards.models import Guard

OCCURRENCES_URL = reverse('occurrences-list')


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


def sample_occurrence(user, guard, created_at=date.today(), _status=0):
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


def detail_url(occurrence_id):
    """Return occurrence detail url"""
    return reverse('occurrences-detail', args=[occurrence_id])


class PublicOccurrenceApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(OCCURRENCES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED,
                         "status code must be 401 UNAUTHORIZED")


class PrivateOccurrenceApiTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='user@email.com',
            password='some_pass'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.guard = sample_guard()

    def test_retrieve_occurrences(self):
        """Test retrieving occurrences"""
        sample_occurrence(self.user, self.guard)
        sample_occurrence(self.user, self.guard)

        res = self.client.get(OCCURRENCES_URL)

        occurrences = Occurrence.objects.filter(user=self.user).order_by('-created_at')
        serializer = OccurrenceSerializer(occurrences, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK,
                         'status code must be 200 OK')
        self.assertEqual(res.data, serializer.data)

    def test_occurrences_limited_to_user(self):
        """Test tetrieving occurrences for user"""
        user2 = get_user_model().objects.create_user(
            'other@lookfish.com',
            'testpass'
        )
        sample_occurrence(user2, self.guard)
        sample_occurrence(self.user, self.guard)

        res = self.client.get(OCCURRENCES_URL)

        occurrences = Occurrence.objects.filter(user=self.user)
        serializer = OccurrenceSerializer(occurrences, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK,
                         'status code must be 200 OK')
        self.assertEqual(len(res.data), 1, 'len(res.data) must be 1')
        self.assertEqual(res.data, serializer.data,
                         'res.data must be equal serializer.data')

    def test_view_occurrence_detail(self):
        """Test viewing a occurrence detail"""
        occurrence = sample_occurrence(self.user, self.guard)
        occurrence2 = sample_occurrence(self.user, self.guard)

        url = detail_url(occurrence.id)
        res = self.client.get(url)

        serializer = OccurrenceSerializer(occurrence)
        self.assertEqual(res.data, serializer.data,
                         'res.data must be equal serializer.data')

    def test_create_occurrence(self):
        """Test creating occurrence"""
        payload = {
            'license_plate': 'abc0000',
            'occurrence_type': 'Batida',
            'occurrence_title': 'Me bateram aqui aaa',
            'location': 'Rua 2 do bairro 1',
            'created_at': date.today().strftime('%Y-%m-%d')
        }

        res = self.client.post(OCCURRENCES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED,
                         'status code must be 201 CREATED')
        occurrence = Occurrence.objects.get(id=res.data['id'])
        for key, value in payload.items():
            self.assertEqual(res.data[key], value,
                             'payload must be equals res.data')

    def test_partial_update(self):
        """Test updating a occurrence with patch"""
        occurrence = sample_occurrence(self.user, self.guard)

        payload = {
            'occurrence_title': 'Me barruaram',
            'created_at': date.today() - timedelta(2)
            }
        url = detail_url(occurrence.id)
        self.client.patch(url, payload)

        occurrence.refresh_from_db()
        self.assertEqual(occurrence.occurrence_title, payload['occurrence_title'])
        self.assertEqual(occurrence.created_at, payload['created_at'])
    
    def test_full_update(self):
        """Test updating a occurrence with put"""
        occurrence = sample_occurrence(self.user, self.guard)
        payload = {
            'license_plate': 'bdc2019',
            'occurrence_type': 'estacionamento proibido',
            'occurrence_title': 'Estacionaram na frente da minha garagem',
            'location': 'Rua 1 do bairro 2',
            'created_at': date.today() - timedelta(2),
        }

        url = detail_url(occurrence.id)
        self.client.put(url, payload)

        occurrence.refresh_from_db()

        self.assertEqual(occurrence.license_plate, payload['license_plate'])
        self.assertEqual(occurrence.occurrence_type, payload['occurrence_type'])
        self.assertEqual(occurrence.occurrence_title, payload['occurrence_title'])
        self.assertEqual(occurrence.location, payload['location'])
        self.assertEqual(occurrence.created_at, payload['created_at'])

    def test_delete_occurrence(self):
        occurrence = sample_occurrence(self.user, self.guard)

        url = detail_url(occurrence.id)
        self.client.delete(url)

        occurrences = list(Occurrence.objects.all())
        self.assertEqual(len(occurrences), 0)
