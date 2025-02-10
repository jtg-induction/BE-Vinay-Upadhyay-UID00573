from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions

from .models import Todo
from .serializers import TodoApiViewSetCreateSerializer, TodoViewSetSerialzer


class TodoAPIViewSet(ModelViewSet):
    """
        success response for create/update/get
        {
          "name": "",
          "done": true/false,
          "date_created": ""
        }

        success response for list
        [
          {
            "name": "",
            "done": true/false,
            "date_created": ""
          }
        ]
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        todo_api_viewset_serializer = TodoViewSetSerialzer
        if self.action == 'create':
             todo_api_viewset_serializer = TodoApiViewSetCreateSerializer
        return todo_api_viewset_serializer
    
    def get_queryset(self):
        user_id = self.request.user.id
        todo_objects = Todo.objects.filter(user_id=user_id)
        return todo_objects
    