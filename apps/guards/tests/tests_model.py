from django.test import TestCase
from apps.guards.models import Guard


class GuardModelTests(TestCase):
    def test_create_complete_guard_model(self):
        """Test creating a new guard with all fields"""
        payload = {
            "name": "junin",
            "cod_guard": "123",
        }
        guard = Guard.objects.create(**payload)
        self.assertEqual(str(guard), guard.name, 'str guard must return the name')
        for key in payload.keys():
            self.assertEqual(
                payload[key], getattr(guard, key),
                f'{key}, must be {payload[key]}'
            )

    def test_guard_with_existing_cod_guard(self):
        Guard.objects.create(cod_guard="123")
        with self.assertRaises(Exception) as context:
            Guard.objects.create(cod_guard="123")
        self.assertTrue('UNIQUE constraint failed: guards_guard.cod_guard' in str(context.exception),
                        'must rise that cod_guard must be unique')
