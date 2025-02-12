from rest_framework import serializers
from .models import ProjectMember, Project
from django.contrib.auth import get_user_model

 # Fetch the Custom User model

class ProjectMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectMember
        fields = ['project_id', 'member_id']  
            