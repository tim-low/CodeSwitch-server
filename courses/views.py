from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import action

import re

from utils import get_or_none

from .models import Course
from .serializers import CourseSerializer

# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):
    """API endpoints pertaining to interests.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

# ====================================================================================================================

import json
import requests

def get_access_token():
    """get SF access token
    
    Returns:
        string -- access token
    """
    HEADERS = {
        "Authorization" : "Basic MWJiMWVmNGIyNDRlNGU5Y2I2YjdhZjVjYmM5YWZiMzc6TTJGa1lqSXpNbVV0TkdOaFpTMDBaVGczTFdJeU5tUXRaakUwT1dZd1ltUmhaalV3", # Basic base64encode(Client_ID:Secret)
        "Content-Type" : "application/x-www-form-urlencoded"   
    }

    DATA = {
        "grant_type" : "client_credentials"
    }

    URL = "https://public-api.ssg-wsg.sg/dp-oauth/oauth/token"

    access_token = requests.post(url=URL, headers = HEADERS, data= DATA)
    return access_token.json()['access_token']

def getFilteredCourses(r):
    """get courses that are filtered
    
    Arguments:
        r {request} -- request object
    
    Returns:
        string[] -- i think it's a string of dictionaries
    """
    filteredCourses = []

    courses = r['data']['courses']
    for course in courses:
        this_course_data = {k:course[k] for k in ('referenceNumber','trainingProviderAlias','title', 'displayImageName') if k in course}
        this_course_data['modeOfTrainings'] = course['modeOfTrainings'][0]['description']
        filteredCourses.append(this_course_data)
    
    return filteredCourses

def getFilteredData(r):
    """get filtered data?
    
    Arguments:
        r {request} -- request object
    
    Returns:
        string[] -- aha
    """

    details = r['data']['courses'][0]
    
    # print (details , "\n")
    
    fieldsToKeep = ['referenceNumber','title', 'trainingProviderAlias', 'objective', 'content','jobLevels','numberOfTrainingDay', 
                'totalTrainingDurationHour', 'totalCostOfTrainingPerTrainee', 'url', 
                'skillsFutureCreditReferenceNumber', 'skillsConnectReferenceNumber', 'displayImageName']

    
    filteredData = {k:details[k] for k in fieldsToKeep if k in details}
    filteredData['dateStart'] = details['support'][0]['period']['from']
    filteredData['dateEnd'] = details['support'][0]['period']['to']
    filteredData['phoneNumber'] = details['contactPerson'][0]['telephone']['number']
    filteredData['email'] = details['contactPerson'][0]['email']['full']
    filteredData['modeOfTrainings'] = details['modeOfTrainings'][0]['description']
    filteredData['createDate'] = details['meta']['createDate']
    
    return filteredData

def get_courses(request):
    # mode = event['queryStringParameters']['searchOrDetails']
    mode = request.GET.get('searchOrDetails')
    print(mode)

    response = None

    try:
        if mode == "search":
            
            keyword = request.GET.get('keyword')
            
            URL = "https://public-api.ssg-wsg.sg/courses/directory"
        
            HEADERS = {
                "Authorization" : "Bearer " + get_access_token()
            }
            
            PARAMS = {
                "pageSize": 10,
                "page" : 0 ,
                "keyword" : keyword
            }
            
            r = requests.get(url = URL, headers=HEADERS, params = PARAMS).json()
            filteredCourses = getFilteredCourses(r)

            response = {
                'statusCode': 200,
                'body': filteredCourses
            }
        
        elif mode=="details":
            
            referenceNumber = request.GET.get('referenceNumber')
            print(referenceNumber)
            
            URL = "https://public-api.ssg-wsg.sg/courses/directory/" + referenceNumber
            # courses/directory/{course reference number}
            
            HEADERS = {
                "Authorization" : "Bearer " + get_access_token()
            }
            
            r = requests.get(url = URL, headers=HEADERS).json()
            
            filteredData = getFilteredData(r)
            
            response = {
                'statusCode': 200,
                'body': filteredData
            }
        return JsonResponse(response, safe=False)

    except:
        return JsonResponse({"statusCode": 404})
        

# event = {'queryStringParameters': {"searchOrDetails" : "search", "keyword" : "knitting"}}
# event = {'queryStringParameters': {"searchOrDetails" : "details", "referenceNumber" : "NP-T08GB0039A-01-NP_SFDA08"}}
# print (lambda_handler(event, None))
    
    