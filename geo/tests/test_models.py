from django.test import TestCase
from django.contrib.auth import get_user_model

from geo import models


def sample_user(email='test@test.com', password='123'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


def sample_state(user, name='Minas Gerais', initials='MG'):
    """Create a sample user"""
    return models.State.objects.create(name=name, initials=initials, user=user)


class ModelTests(TestCase):
    def test_state_str(self):
        """Test the state string representation"""
        state = models.State.objects.create(
            user=sample_user(),
            name='Minas Gerais',
            initials='MG',
        )

        self.assertEqual(str(state), state.name)

    def test_court_district_str(self):
        """Test the court district string representation"""
        user = sample_user()
        state = sample_state(user)

        court_district = models.CourtDistrict.objects.create(
            user=user,
            name='Belo Horizonte',
            state=state,
        )

        self.assertEqual(str(court_district), court_district.name)
