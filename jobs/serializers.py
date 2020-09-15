from .models import Job, SavedJob
from skills.models import Skill
from interests.models import Interest
from courses.models import Course
from users.models import ModifiedUser

from rest_framework import serializers

class JobSerializer(serializers.ModelSerializer):
    required_skills = serializers.SlugRelatedField(many=True, slug_field="name", queryset=Skill.objects.all())

    class Meta:
        model = Job
        fields = '__all__'

class SavedJobSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=ModifiedUser.objects.all())

    class Meta:
        model = SavedJob
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(SavedJobSerializer, self).to_representation(instance)
        representation['job'] = JobSerializer(instance.job).data
        return representation