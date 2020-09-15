from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from django.http import HttpResponseRedirect
from django.db.models import Q

import re
from datetime import datetime, timedelta
import random

from utils import get_or_none
from .models import Job, SavedJob
from skills.models import Skill
from .serializers import JobSerializer, SavedJobSerializer

class JobViewSet(viewsets.ModelViewSet):
    """API endpoints pertaining to jobs.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer

# Get jobs for specific user.
class SavedJobList(generics.ListAPIView):
    serializer_class = SavedJobSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        queryset = SavedJob.objects.filter(user__id=user_id).order_by('has_applied')
        return queryset

class JobQueryList(generics.ListAPIView):
    serializer_class = JobSerializer
    
    def get_queryset(self):
        queryset = Job.objects.all()
        q = self.request.query_params.get('q', None)
        if q is not None:
            queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(company__icontains=q)).order_by('-date_posted')

        return queryset

class SavedJobViewSet(viewsets.ModelViewSet):
    """API endpoints pertaining to user-jobs.
    """
    queryset = SavedJob.objects.all()
    serializer_class = SavedJobSerializer

def generate_skills(request):
    # job = Job.objects.get(id=1) 

    for job in Job.objects.all():
        # date = generate_date()
        # job.date_posted = date
        # job.save()
        desc = job.description
        for skill in Skill.objects.all():
            if (skill.name.lower() in desc) or (skill.name in desc):
                job.required_skills.add(skill.id)
        job.save()
        print("aaa")

    return HttpResponseRedirect('')

def generate_date():
    start = datetime(2019, 12, 1)
    end = start + timedelta(days=115)
    return (start + (end - start) * random.random()).strftime("%Y-%m-%d")

def import_db(request):
    f = open('dump.csv', 'r', encoding="mac_roman")
    j = 0
    for line in f:
        line =  line.split('|')
        date = generate_date()

        tempDesc = line[2].replace("'", "").replace('"', '')
        if len(tempDesc) < 1000:
            continue

        tmp = Job.objects.create(title="", company="", description="", date_posted=date, 
                                application_src="http://www.placeholder.com")
        for i in range(4):
            print(line[i].replace("'", ""))
        tmp.title = line[0].replace("'", "")
        tmp.company = line[1].replace("'", "")
        tmp.description = tempDesc
        tmp.application_src = line[3].replace("'", "").replace("\n", '')
        tmp.save()
        if j == 1000:
            break
        j += 1

    f.close()
    return HttpResponseRedirect('')