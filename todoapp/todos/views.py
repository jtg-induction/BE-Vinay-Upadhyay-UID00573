from rest_framework import serializers, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.viewsets import ModelViewSet

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
    def get_serializer_class(self):
        if self.action == 'create':
             return TodoApiViewSetCreateSerializer
        return TodoViewSetSerialzer
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id',None)
        if user_id is not None:
            return Todo.objects.filter(user__id=user_id)
        return Todo.objects.all()