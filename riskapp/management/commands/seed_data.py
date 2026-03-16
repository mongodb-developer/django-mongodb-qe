from django.core.management.base import BaseCommand
from django.db import transaction

from riskapp.models import (
    RiskAssessment,
    Risk,
    RiskCategory,
    RiskOwner,
)

ASSESSMENTS = [
    {
        "risk_title": "NoSQL Injection",
        "risk_description": "Potential NoSQL injection via unsanitised operators",
        "category": "Security",
        "cat_desc": "Security and authentication data",
        "likelihood": "High",
        "impact": "High",
        "score": 9,
    },
    {
        "risk_title": "Data Exposure",
        "risk_description": "Sensitive data returned without field projection",
        "category": "Personal",
        "cat_desc": "Personal identifiable information (PII)",
        "likelihood": "Medium",
        "impact": "High",
        "score": 7,
    },
    {
        "risk_title": "Privilege Escalation",
        "risk_description": "Attempt to modify roles or permissions",
        "category": "Security",
        "cat_desc": "Security and authentication data",
        "likelihood": "Low",
        "impact": "High",
        "score": 6,
    },
    {
        "risk_title": "GDPR Violation",
        "risk_description": "Query accesses EU citizen data without consent check",
        "category": "Compliance",
        "cat_desc": "Regulatory and compliance data",
        "likelihood": "Medium",
        "impact": "Medium",
        "score": 5,
    },
    {
        "risk_title": "PHI Exposure",
        "risk_description": "Protected health information returned in query",
        "category": "Healthcare",
        "cat_desc": "Medical and health records (PHI)",
        "likelihood": "High",
        "impact": "High",
        "score": 9,
    },
    {
        "risk_title": "Credit Card Leak",
        "risk_description": "Payment card data queried without masking",
        "category": "Financial",
        "cat_desc": "Financial data and transactions",
        "likelihood": "Medium",
        "impact": "High",
        "score": 8,
    },
    {
        "risk_title": "Mass Data Export",
        "risk_description": "Query fetches excessive number of documents",
        "category": "Compliance",
        "cat_desc": "Regulatory and compliance data",
        "likelihood": "Low",
        "impact": "Medium",
        "score": 4,
    },
    {
        "risk_title": "Unindexed Scan",
        "risk_description": "Collection scan on sensitive collection",
        "category": "Financial",
        "cat_desc": "Financial data and transactions",
        "likelihood": "High",
        "impact": "Low",
        "score": 3,
    },
]


class Command(BaseCommand):
    """
    Seed the database with sample risk assessment data.
    Use --target flush to clear data before reseeding.
    """

    help = "Seed the database with sample risk assessment data"

    def add_arguments(self, parser):
        parser.add_argument(
            '--target',
            default='all',
            choices=['all', 'default', 'encrypted', 'flush'],
            help="'flush' to clear data, 'all' to seed both, or specify a database",
        )

    def handle(self, *args, **options):
        target = options['target']

        if target == 'flush':
            self._flush('default')
            self._flush('encrypted')
            return

        if target == 'all':
            databases = ['default', 'encrypted']
        else:
            databases = [target]

        try:
            for db in databases:
                self.db = db
                self.stdout.write(f"\nSeeding into: {self.db}")
                with transaction.atomic(using=self.db):
                    self._seed_assessments()
            self.stdout.write(self.style.SUCCESS("\nAll data seeded successfully!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"\nSeeding failed: {e}"))

    def _flush(self, db):
        RiskAssessment.objects.using(db).all().delete()
        self.stdout.write(self.style.WARNING(f"Flushed data from: {db}"))

    def _seed_assessments(self):
        self.stdout.write("\n--- Seeding Risk Assessments ---")

        owner = RiskOwner(
            username="assessor",
            email="assessor@querysafe.com",
            role="Analyst",
        )

        for item in ASSESSMENTS:
            assessment = RiskAssessment(
                risk=Risk(
                    title=item["risk_title"],
                    description=item["risk_description"],
                    category=RiskCategory(
                        name=item["category"],
                        description=item["cat_desc"],
                    ),
                ),
                owner=owner,
                likelihood=item["likelihood"],
                impact=item["impact"],
                score=item["score"],
            )
            assessment.save(using=self.db)
            self.stdout.write(
                f"  Created: {item['risk_title']} ({item['likelihood']}/{item['impact']})"
            )
