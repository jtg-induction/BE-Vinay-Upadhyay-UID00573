from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.postgres.aggregates import ArrayAgg


from projects.models import Project
from users.models import CustomUser
from projects.models import ProjectMember

 # Fetch the Custom User model

class ProjectMemberSerializer(serializers.ModelSerializer):
    user_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=CustomUser.objects.all(), write_only=True)
    
    class Meta:
        model = Project
        fields = ['user_ids'] 

    def update(self, instance, validated_data):
        action = self.context['action']
        validated_user_ids = [user.id for user in validated_data['user_ids']]
        project_member_list = instance.members.values_list('id', flat=True)
        
        log = {}
        
        if action == 'add':
            user_projects = list(get_user_model().objects.filter(id__in=validated_user_ids).annotate(
                project_ids = ArrayAgg('allprojects__id'
            )))
            print(user_projects[0].project_ids)
            project_member_instance = []
            
            for user in user_projects:
                if len(project_member_list)>instance.max_members:
                    log[user.id] = 'Project member reach maximum limit'
                elif len(user.project_ids)>=2:
                    log[user.id] = 'User can\'t be part of more than two projects'
                elif instance.id in user.project_ids:
                    log[user.id] = 'project_id already map to member_id'
                else:
                    project_member_instance.append(ProjectMember(project=instance, member=user))
                    log[user.id] = 'added successfully'
          
            ProjectMember.objects.bulk_create(project_member_instance)
        
        else:
            for user_id in validated_user_ids:
                if user_id in project_member_list:
                    ProjectMember.objects.filter(project_id=instance.id, member_id=user_id).delete()
                    log[user_id] = 'deleted successfully'
                else:
                    log[user_id] = 'user is not a member'
        
        self.context['log'] = log

        return instance
    
    def to_representation(self, instance):
        data = {}
        data['log'] = self.context['log']
        return data
