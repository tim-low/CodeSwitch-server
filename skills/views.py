from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, generics
from rest_framework.decorators import action

import re
import json

from utils import get_or_none

from .models import Skill
from .serializers import SkillSerializer

class SkillViewSet(viewsets.ModelViewSet):
    """API endpoints pertaining to skills.
    """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

    @action(methods=['get'], detail=False, url_path='groups')
    @csrf_exempt
    def get_list_of_groups(self, request):
        """Get list of all unique groups.
        """

        groups = list(Skill.objects.all().values('group').distinct())
        ret = [d['group'] for d in groups]

        return JsonResponse(ret, safe=False)

    @action(methods=['get'], detail=False, url_path='filter')
    def get_skills_in_group(self, request, **kwargs):
        print(self.get_queryset())
        return HttpResponseRedirect('')


class SkillInGroupList(generics.ListAPIView):
    serializer_class = SkillSerializer
    
    def get_queryset(self):
        queryset = Skill.objects.all()
        q = self.request.query_params.get('q', None)

        if q is not None:
            queryset = queryset.filter(group=q)

        return queryset