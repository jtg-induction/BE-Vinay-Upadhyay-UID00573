from django.contrib.auth import get_user_model
from rest_framework import serializers
from todos.models import Todo
from users.serializers import UserSerializer
from projects.models import Project
from django.db.models import Count, Q
from users.models import CustomUser


class TodoSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(
        source='date_created', format="%I:%M %p, %d %b, %Y")
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return "Done" if obj.done else "To Do"

    def get_creator(self, obj):
        creater_data = UserSerializer(obj.user).data
        creater_data.pop('id')
        return creater_data

    class Meta:
        model = Todo
        fields = ['id', 'name', 'status', 'creator', 'created_at']

# serializer for status


class StatusSerialiser(serializers.ModelSerializer):
    completed_count = serializers.IntegerField()
    pending_count = serializers.IntegerField()

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name',
                  'email', 'completed_count', 'pending_count']


# Serializers of maxpending
class MaxStatusSerializer(serializers.ModelSerializer):
    pending_count = serializers.IntegerField()

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'pending_count']


class ProjectWiseReportSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source='name')
    report = serializers.SerializerMethodField()

    def get_report(self, obj):
        report = []
        for details in obj.reports:
            detailed_dict = {
                "first_name": details.first_name,
                "last_name": details.last_name,
                "email": details.email,
                "pending_count": details.pending_count,
                "completed_count": details.completed_count,
            }
            report.append(detailed_dict)
        return report

    class Meta:
        model = Project
        fields = ['project_title', 'report']


class TodoWithInDateRange(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    creator = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(
        source='date_created', format='%I:%M %p, %d %b, %Y')

    def get_status(self, obj):
        return "Done"

    def get_creator(self, obj):
        return obj.user.first_name + " " + obj.user.last_name

    def get_email(self, obj):
        return obj.user.email

    class Meta:
        model = Todo
        fields = ['id', 'name', 'creator', 'email', 'created_at', 'status']


class MemberStartWithEndA(serializers.ModelSerializer):
    project_name = serializers.CharField(source='name')
    done = serializers.SerializerMethodField()

    def get_done(self, obj):
        if obj.status == 1 or obj.status == 0:
            return False
        elif obj.status == 2:
            return True

    class Meta:
        model = Project
        fields = ['project_name', 'done', 'max_members']


class ProjectDetailsSerializer(serializers.ModelSerializer):
    existing_member_count = serializers.IntegerField()
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        if obj.status == 0:
            return "To be started"
        elif obj.status == 1:
            return "In progress"
        else:
            return "Completed"

    class Meta:
        model = Project
        fields = ['id', 'name', 'status',
                  'existing_member_count', 'max_members']


class UserWiseProjectStatusSerializer(serializers.ModelSerializer):
    to_do_projects = serializers.SerializerMethodField()
    in_progress_projects = serializers.SerializerMethodField()
    completed_projects = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'to_do_projects',
                  'in_progress_projects', 'completed_projects']

    def get_to_do_projects(self, obj):
        return obj.to_do if obj.to_do else []

    def get_in_progress_projects(self, obj):
        return obj.in_progress if obj.in_progress else []

    def get_completed_projects(self, obj):
        return obj.completed if obj.completed else []
