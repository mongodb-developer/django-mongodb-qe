from rest_framework import serializers

RISK_LEVEL_CHOICES = ["Low", "Medium", "High"]


class RiskCategorySerializer(serializers.Serializer):

    name = serializers.CharField(max_length=100)
    description = serializers.CharField(
        max_length=500, required=False, default=""
    )


class RiskSerializer(serializers.Serializer):

    title = serializers.CharField(max_length=200)
    description = serializers.CharField(
        max_length=500, required=False, default=""
    )
    category = RiskCategorySerializer()


class RiskOwnerSerializer(serializers.Serializer):
    """Serializer for owner input (embedded in assessment)."""

    username = serializers.CharField(max_length=150)
    email = serializers.CharField(max_length=254, required=False, default="")
    role = serializers.CharField(max_length=100, required=False, default="")


class AssessmentSerializer(serializers.Serializer):

    risk = RiskSerializer()
    owner = RiskOwnerSerializer(required=False)
    likelihood = serializers.ChoiceField(choices=RISK_LEVEL_CHOICES)
    impact = serializers.ChoiceField(choices=RISK_LEVEL_CHOICES)
    score = serializers.IntegerField(min_value=1, max_value=10)


class AssessmentResponseSerializer(serializers.Serializer):

    id = serializers.CharField(source='pk', read_only=True)
    risk = RiskSerializer()
    owner = RiskOwnerSerializer()
    likelihood = serializers.CharField()
    impact = serializers.CharField()
    score = serializers.IntegerField()
    assessed_on = serializers.DateField()
