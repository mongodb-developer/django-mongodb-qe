"""Tests for the Risk Assessment API."""

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from riskapp.models import RiskAssessment, Risk, RiskCategory, RiskOwner

DB = 'encrypted'
URL = '/api/assessments/'

VALID_PAYLOAD = {
    "risk": {
        "title": "Test Risk",
        "description": "Test description",
        "category": {
            "name": "Security",
            "description": "Security data",
        },
    },
    "owner": {
        "username": "tester",
        "email": "tester@querysafe.com",
        "role": "Analyst",
    },
    "likelihood": "High",
    "impact": "High",
    "score": 9,
}


def seed(db=DB):
    """Create a test assessment directly in the database."""
    return RiskAssessment(
        risk=Risk(
            title="Test Risk",
            description="Test description",
            category=RiskCategory(name="Security", description="Security data"),
        ),
        owner=RiskOwner(username="tester", email="tester@querysafe.com", role="Analyst"),
        likelihood="High",
        impact="High",
        score=9,
    ).save(using=db)


class AssessmentTests(TestCase):
    """Tests for /api/assessments/ endpoint."""

    databases = {DB}

    def setUp(self):
        self.client = APIClient()

    def test_list_empty(self):
        res = self.client.get(URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json(), [])

    def test_list_returns_data(self):
        seed()
        res = self.client.get(URL)
        self.assertEqual(len(res.json()), 1)
        self.assertEqual(res.json()[0]["risk"]["title"], "Test Risk")

    def test_create_valid(self):
        res = self.client.post(URL, VALID_PAYLOAD, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RiskAssessment.objects.using(DB).count(), 1)

    def test_create_missing_risk(self):
        payload = {**VALID_PAYLOAD}
        del payload["risk"]
        res = self.client.post(URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_likelihood(self):
        payload = {**VALID_PAYLOAD, "likelihood": "Critical"}
        res = self.client.post(URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_score_out_of_range(self):
        payload = {**VALID_PAYLOAD, "score": 11}
        res = self.client.post(URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_encrypted_round_trip(self):
        self.client.post(URL, VALID_PAYLOAD, format="json")
        res = self.client.get(URL)
        data = res.json()[0]
        self.assertEqual(data["risk"]["title"], "Test Risk")
        self.assertEqual(data["owner"]["username"], "tester")
