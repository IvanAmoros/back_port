from rest_framework import serializers
from .models import Comment, TechnicalSkillCategory, TechnicalSkill, WorkExperience, Studies


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
    from_date = serializers.DateField(format="%d/%m/%Y", input_formats=['%d/%m/%Y', 'iso-8601'])
    to_date = serializers.DateField(format="%d/%m/%Y", input_formats=['%d/%m/%Y', 'iso-8601'], required=False, allow_null=True)

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


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['name', 'text', 'accepted', 'web_url', 'linkedin_url', 'github_url', 'created']
        #extra_kwargs = {'accepted': {'write_only': True}} # Make accepted write-only to hide it in responses by default

    def __init__(self, *args, **kwargs):
        # Call the superclass init
        super(CommentSerializer, self).__init__(*args, **kwargs)
        
        # Check for 'request' in the context and then the user's admin status
        request = self.context.get('request', None)
        if request and not request.user.is_superuser:
            # Remove the 'accepted' field for non-admin users
            self.fields.pop('accepted', None)
        if request and not request.user.is_active:
            self.fields.pop('web_url', None)
            self.fields.pop('linkedin_url', None)
            self.fields.pop('github_url', None)
            self.fields.pop('name', None)

    