from rest_framework import serializers

from .models import Course
from skills.models import Skill

class CourseSerializer(serializers.ModelSerializer):
    skills_taught = serializers.SlugRelatedField(many=True, slug_field="name", queryset=Skill.objects.all())

    class Meta:
        model = Course
        fields = '__all__'
