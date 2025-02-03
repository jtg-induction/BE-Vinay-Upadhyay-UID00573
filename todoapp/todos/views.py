from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .serializers import TodoApiViewSetSerializer
from rest_framework.settings import api_settings
from .serializers import TodoUpdateSerializer
from .models import Todo


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
    queryset = Todo.objects.all()
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return TodoUpdateSerializer
        return TodoApiViewSetSerializer
