from django.urls import path
from projects.views import ProjectMemberApiViewSet

app_name = 'projects'

urlpatterns=[path('projectmember/', ProjectMemberApiViewSet.as_view(), name='projectmember'),]
