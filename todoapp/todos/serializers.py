from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from rest_framework import serializers


from projects import models as projects_models
from todos import models as todos_models
from users import models as users_models
from users.serializers import UserBaseSerializer, UserSerializer


class TodoSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(
        source='date_created', format="%I:%M %p, %d %b, %Y"
    )
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return "Done" if obj.done else "To Do"

    def get_creator(self, obj):
        creater_data = UserBaseSerializer(obj.user).data
        return creater_data

    class Meta:
        model = todos_models.Todo
        fields = ['id', 'name', 'status', 'creator', 'created_at']


class StatusSerialiser(serializers.ModelSerializer):
    completed_count = serializers.IntegerField()
    pending_count = serializers.IntegerField()

    class Meta:
        model = users_models.CustomUser
        fields = ['id', 'first_name', 'last_name',
                  'email', 'completed_count', 'pending_count']


class MaxStatusSerializer(serializers.ModelSerializer):
    pending_count = serializers.IntegerField()

    class Meta:
        model = users_models.CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'pending_count']


class ProjectReportSerializer(serializers.ModelSerializer):
    pending_count = serializers.IntegerField()
    completed_count = serializers.IntegerField()

    class Meta:
        model = users_models.CustomUser
        fields = ["first_name", "last_name", "email", "pending_count", "completed_count"]
            

class ProjectWiseReportSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source='name')
    report = ProjectReportSerializer(source="reports", many=True, read_only=True)

    class Meta:
        model = projects_models.Project
        fields = ['project_title', 'report']


class TodoWithInDateRangeSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    creator = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(
        source='date_created', format='%I:%M %p, %d %b, %Y'
    )

    def get_status(self, obj):
        return "Done" if obj.done else "Pending"
       
    def get_creator(self, obj):
        return obj.user.first_name + " " + obj.user.last_name

    def get_email(self, obj):
        return obj.user.email

    class Meta:
        model = todos_models.Todo
        fields = ['id', 'name', 'creator', 'email', 'created_at', 'status']


class MemberStartWithEndASerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='name')
    done = serializers.SerializerMethodField()

    def get_done(self, obj):
        if obj.status == 1 or obj.status == 0:
            return False
        elif obj.status == 2:
            return True

    class Meta:
        model = projects_models.Project
        fields = ['project_name', 'done', 'max_members']


class ProjectDetailsSerializer(serializers.ModelSerializer):
    existing_member_count = serializers.IntegerField()
    status = serializers.ChoiceField(choices=projects_models.Project.STATUS_CHOICES)

    class Meta:
        model = projects_models.Project
        fields = ['id', 'name', 'status',
                  'existing_member_count', 'max_members']


class UserWiseProjectStatusSerializer(serializers.ModelSerializer):
    to_do_projects = serializers.SerializerMethodField()
    in_progress_projects = serializers.SerializerMethodField()
    completed_projects = serializers.SerializerMethodField()

    class Meta:
        model = users_models.CustomUser
        fields = ['first_name', 'last_name', 'email', 'to_do_projects',
                  'in_progress_projects', 'completed_projects']

    def get_to_do_projects(self, obj):
        return obj.to_do if obj.to_do else []

    def get_in_progress_projects(self, obj):
        return obj.in_progress if obj.in_progress else []

    def get_completed_projects(self, obj):
        return obj.completed if obj.completed else []
    

class TodoApiViewSetCreateSerializer(serializers.ModelSerializer):
    todo = serializers.CharField(source='name')
    user_id = serializers.PrimaryKeyRelatedField(source='user', queryset = get_user_model().objects.all())

    class Meta:
        model = todos_models.Todo
        fields = ['user_id', 'todo']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        return {
                "name": representation["todo"],
                "done" : instance.done,
                "Date_created" : instance.date_created.isoformat()
            }
    

class TodoViewSetSerialzer(serializers.ModelSerializer):
    todo_id = serializers.IntegerField(source='id')
    todo = serializers.CharField(source='name')

    class Meta:
        model = todos_models.Todo
        fields = ['todo_id', 'todo', 'done']    