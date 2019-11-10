from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from geo.models import CourtDistrict, State

from geo.serializers import CourtDistrictSerializer

# app:identifier for the url in the app
COURT_DISTRICT_URL = reverse('geo:courtdistrict-list')


# /api/court-district/court-districts/1/
def detail_url(court_district_id):
    """Return court district detail URL"""
    return reverse('geo:courtdistrict-detail', args=[court_district_id])


def sample_state(user, name='Minas Gerais', initials='MG'):
    """Create and return a sample state"""
    return State.objects.create(user=user, name=name, initials=initials)


def sample_court_district(user, name, state):
    """Create an return a sample court district"""
    return CourtDistrict.objects.create(user=user, name=name, state=state)


class PublicCourtDistrictAPITests(TestCase):
    """Test unauthenticated court district API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(COURT_DISTRICT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCourtDistrictAPITests(TestCase):
    """Test authenticated court district API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'teste@teste.com',
            '123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_court_districts(self):
        """Test retrieving a list of court districts"""
        state = sample_state(user=self.user, name='Minas Gerais',
                             initials='MG')
        sample_court_district(user=self.user, name='Belo Horizonte',
                              state=state)
        state = sample_state(user=self.user, name='Bahia',
                             initials='BA')
        sample_court_district(user=self.user, name='Salvador',
                              state=state)

        res = self.client.get(COURT_DISTRICT_URL)

        court_districts = CourtDistrict.objects.all().order_by('-id')
        # many=True - returns results as a list
        serializer = CourtDistrictSerializer(court_districts, many=False)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_court_districts_limited_to_user(self):
        """Test retrieving court districts for user"""
        user2 = get_user_model().objects.create_user(
            'teste2@teste.com',
            '123'
        )

        state = sample_state(user=user2, name='Minas Gerais',
                             initials='MG')
        sample_court_district(user=user2, name='Belo Horizonte',
                              state=state)
        state = sample_state(user=self.user, name='Bahia',
                             initials='BA')
        sample_court_district(user=self.user, name='Salvador',
                              state=state)

        res = self.client.get(COURT_DISTRICT_URL)

        court_districts = CourtDistrict.objects.filter(user=self.user)
        serializer = CourtDistrictSerializer(court_districts, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_court_district_detail(self):
        """Test a viewing a court district detail"""
        state = sample_state(user=self.user, name='Bahia',
                             initials='BA')
        court_district = sample_court_district(
            user=self.user,
            name='Salvador',
            state=state)

        url = detail_url(court_district.id)
        res = self.client.get(url)

        serializer = CourtDistrictSerializer(court_district)
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_court_district(self):
        """Test creating court district"""
        payload = {
            'name': 'Belo Horizonte',
            'state': sample_state(user=self.user),
            'user': self.user
        }

        res = self.client.post(COURT_DISTRICT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        court_district = CourtDistrict.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(court_district, key))

