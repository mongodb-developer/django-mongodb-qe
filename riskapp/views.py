
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from riskapp.models import (
    RiskAssessment,
    Risk,
    RiskCategory,
    RiskOwner,
)
from riskapp.serializers import (
    AssessmentSerializer,
    AssessmentResponseSerializer,
)

DB = 'encrypted'


class AssessmentView(APIView):

    @extend_schema(
        responses=AssessmentResponseSerializer(many=True),
        summary="List all assessments",
        tags=["Assessments"],
    )
    def get(self, request):
        assessments = RiskAssessment.objects.using(DB).all()
        serializer = AssessmentResponseSerializer(assessments, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=AssessmentSerializer,
        responses=AssessmentResponseSerializer,
        summary="Create an assessment",
        tags=["Assessments"],
    )
    def post(self, request):
        serializer = AssessmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        risk_data = data['risk']
        category_data = risk_data['category']

        assessment = RiskAssessment(
            risk=Risk(
                title=risk_data['title'],
                description=risk_data.get('description', ''),
                category=RiskCategory(
                    name=category_data['name'],
                    description=category_data.get('description', ''),
                ),
            ),
            likelihood=data['likelihood'],
            impact=data['impact'],
            score=data['score'],
        )

        if data.get('owner'):
            owner_data = data['owner']
            assessment.owner = RiskOwner(
                username=owner_data['username'],
                email=owner_data.get('email', ''),
                role=owner_data.get('role', ''),
            )

        assessment.save(using=DB)

        return Response(
            AssessmentResponseSerializer(assessment).data,
            status=status.HTTP_201_CREATED,
        )
