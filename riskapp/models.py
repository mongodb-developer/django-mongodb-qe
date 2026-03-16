from django.db import models
from django_mongodb_backend.models import EmbeddedModel
from django_mongodb_backend.fields import (
    EncryptedCharField,
    EmbeddedModelField,
)


class RiskCategory(EmbeddedModel):
    name = EncryptedCharField(max_length=100)
    description = EncryptedCharField(max_length=500, blank=True)

    def __str__(self):
        return str(self.name)


class RiskOwner(EmbeddedModel):
    username = EncryptedCharField(max_length=150)
    email = EncryptedCharField(max_length=254, blank=True)
    role = EncryptedCharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


class Risk(EmbeddedModel):
    title = EncryptedCharField(max_length=200)
    description = EncryptedCharField(max_length=500, blank=True, default="")
    category = EmbeddedModelField(RiskCategory)

    def __str__(self):
        return str(self.title)


class RiskAssessment(models.Model):
    RISK_LEVEL_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
    ]

    risk = EmbeddedModelField(Risk)
    owner = EmbeddedModelField(RiskOwner, blank=True, null=True)
    likelihood = models.CharField(max_length=10, choices=RISK_LEVEL_CHOICES)
    impact = models.CharField(max_length=10, choices=RISK_LEVEL_CHOICES)
    score = models.PositiveSmallIntegerField()
    assessed_on = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "risk_assessments"
        ordering = ["-assessed_on"]
        indexes = [
            models.Index(fields=["likelihood"]),
            models.Index(fields=["impact"]),
            models.Index(fields=["score"]),
        ]

    def __str__(self):
        return f"{self.risk.title} ({self.likelihood}/{self.impact})"
