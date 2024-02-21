from rest_framework import serializers
from .models import TechnicalSkillCategory, TechnicalSkill

class TechnicalSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalSkill
        fields = ['id', 'name', 'rating', 'category']

class TechnicalSkillCategorySerializer(serializers.ModelSerializer):
    skills = TechnicalSkillSerializer(many=True, read_only=True)

    class Meta:
        model = TechnicalSkillCategory
        fields = ['id', 'name', 'skills']
