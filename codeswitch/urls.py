from django.urls import include, path
from django.contrib import admin
from rest_framework import routers

import users.views
import skills.views
import interests.views
import courses.views
import jobs.views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', users.views.UserViewSet)
router.register(r'skills', skills.views.SkillViewSet)
# router.register(r'interests', interests.views.InterestViewSet)
# router.register(r'courses', courses.views.CourseViewSet)
router.register(r'jobs', jobs.views.JobViewSet)
router.register(r'saved_jobs', jobs.views.SavedJobViewSet)

urlpatterns = [
    # path('generate_skills', jobs.views.generate_skills),
    # path('import_db', jobs.views.import_db),

    # Get a list of jobs, pass in parameters as query
    path('courses', courses.views.get_courses),
    path('query_jobs', jobs.views.JobQueryList.as_view()),
    path('query_skill_group', skills.views.SkillInGroupList.as_view()),

    # Query saved_jobs to get only the user's
    path('saved_jobs/user/<int:user_id>', jobs.views.SavedJobList.as_view()),

    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]