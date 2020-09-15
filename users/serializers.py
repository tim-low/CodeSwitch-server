from rest_framework import serializers

from .models import ModifiedUser
from skills.serializers import SkillSerializer
from skills.models import Skill
from interests.models import Interest

class UserSerializer(serializers.ModelSerializer):
    skills = serializers.SlugRelatedField(many=True, slug_field="name", queryset=Skill.objects.all())
    # interests = serializers.SlugRelatedField(many=True, slug_field="name", queryset=Interest.objects.all())
    
    class Meta:
        model = ModifiedUser
        fields = ['id', 'email', 'password', 'skills']
