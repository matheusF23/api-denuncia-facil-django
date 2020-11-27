from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from apps.guards.models import Guard


class GuardAdminSiteTests(TestCase):

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

    def test_guards_listed(self):
        """Test that guards are listed on guard page"""
        url = reverse('admin:guards_guard_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.guard.name)
        self.assertContains(res, self.guard.cod_guard)

    def test_guard_change_page(self):
        """Test that the guard edit page works"""
        url = reverse('admin:guards_guard_change', args=[self.guard.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200, 'status code must be 200 OK')

    def test_create_guard_page(self):
        """Test that the create guard page works"""
        url = reverse('admin:guards_guard_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200, 'status code must be 200 OK')
