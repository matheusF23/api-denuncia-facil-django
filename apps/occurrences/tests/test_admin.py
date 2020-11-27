from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from apps.occurrences.models import Occurrence
from apps.guards.models import Guard


class OccurrenceAdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@x9.com',
            password='admintestpass'
        )
        self.client.force_login(self.admin_user)
        self.guard = Guard.objects.create(
            name='Name guard',
            cod_guard='1234',
        )

        self.user = get_user_model().objects.create_user(
            email='test@x9.com',
            password='testpass',
            name='Test user full name'
        )

        self.occurrence = Occurrence.objects.create(
            user=self.user,
            guard=self.guard,
            license_plate='abc2134',
            occurrence_title='bateram aqui',
            occurrence_type='batida',
            location='perto da casa do Joao',
            observation='o cara foi e bateu',
            anonymous=False
        )

    def test_occurrences_listed(self):
        """Test that occurrences are listed on occurrence page"""
        url = reverse('admin:occurrences_occurrence_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.occurrence.license_plate)
        self.assertContains(res, self.occurrence.occurrence_title)
        self.assertContains(res, self.occurrence.occurrence_type)
        self.assertContains(res, self.occurrence.anonymous)
        self.assertContains(res, self.occurrence.status)

    def test_occurrence_change_page(self):
        """Test that the occurrence edit page works"""
        url = reverse('admin:occurrences_occurrence_change', args=[self.occurrence.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200, 'status code must be 200 OK')

    def test_create_occurrence_page(self):
        """Test that the create occurrence page works"""
        url = reverse('admin:occurrences_occurrence_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200, 'status code must be 200 OK')
