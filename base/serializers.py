from rest_framework import serializers

from .models import Comment, TechnicalSkillCategory, TechnicalSkill, WorkExperience, Study


class TechnicalSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalSkill
        fields = ['id', 'name']


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


class StudySerializer(serializers.ModelSerializer):
    skills = TechnicalSkillSerializer(many=True, read_only=True)
    from_date = serializers.DateField(format="%d/%m/%Y", input_formats=['%d/%m/%Y',])
    to_date = serializers.DateField(format="%d/%m/%Y", input_formats=['%d/%m/%Y',], required=False, allow_null=True)

    class Meta:
        model = Study
        fields = ['id', 'center', 'from_date', 'to_date', 'current', 'tittle', 'description', 'skills']


class CommentSerializer(serializers.ModelSerializer):
    responses = serializers.SerializerMethodField()
    created = serializers.DateTimeField(format="%d/%m/%Y %H:%M", read_only=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'accepted', 'web_url', 'linkedin_url', 'github_url', 'created', 'responses']

    def __init__(self, *args, **kwargs):
        super(CommentSerializer, self).__init__(*args, **kwargs)

        request = self.context.get('request', None)
        if request and not request.user.is_superuser:
            self.fields.pop('accepted', None)
        if request and request.method == 'POST' and not request.user.is_active:
            self.fields.pop('web_url', None)
            self.fields.pop('linkedin_url', None)
            self.fields.pop('github_url', None)
            self.fields.pop('user', None)

    def get_responses(self, obj):
        if obj.parent is None:  # Ensure only top-level comments have responses
            responses = obj.responses.filter(accepted=True)
            return ShallowCommentSerializer(responses, many=True, context=self.context).data
        else:
            return []


class ShallowCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    created = serializers.DateTimeField(format="%d/%m/%Y %H:%M", read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'accepted', 'web_url', 'linkedin_url', 'github_url', 'created']
