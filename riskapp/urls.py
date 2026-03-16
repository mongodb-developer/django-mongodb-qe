from django.urls import path
from riskapp.views import AssessmentView

urlpatterns = [
    path('assessments/', AssessmentView.as_view(), name='assessments'),
]
