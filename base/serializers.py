from rest_framework import serializers
from .models import TechnicalSkillCategory, TechnicalSkill, WorkExperience, Studies

class TechnicalSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalSkill
        fields = ['id', 'name', 'rating', 'category']


class TechnicalSkillCategorySerializer(serializers.ModelSerializer):
    skills = TechnicalSkillSerializer(many=True, read_only=True)

    class Meta:
        model = TechnicalSkillCategory
        fields = ['id', 'name', 'skills']



class WorkExperienceSerializer(serializers.ModelSerializer):
    skills = TechnicalSkillSerializer(many=True, read_only=True)
    from_date = serializers.DateField(format="%d/%m/%Y", input_formats=['%d/%m/%Y',])
    to_date = serializers.DateField(format="%d/%m/%Y", input_formats=['%d/%m/%Y',], required=False, allow_null=True)

    class Meta:
        model = WorkExperience
        fields = ['id', 'company', 'from_date', 'to_date', 'current_work', 'position', 'job_tasks', 'skills']


class StudiesSerializer(serializers.ModelSerializer):
    skills = TechnicalSkillSerializer(many=True, read_only=True)
    from_date = serializers.DateField(format="%d/%m/%Y", input_formats=['%d/%m/%Y',])
    to_date = serializers.DateField(format="%d/%m/%Y", input_formats=['%d/%m/%Y',], required=False, allow_null=True)

    class Meta:
        model = Studies
        fields = ['id', 'center', 'from_date', 'to_date', 'current', 'tittle', 'description', 'skills']