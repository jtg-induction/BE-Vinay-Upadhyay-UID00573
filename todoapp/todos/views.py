from rest_framework import serializers, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.viewsets import ModelViewSet

from todos.models import Todo
from todos.serializers import TodoApiViewSetCreateSerializer, TodoViewSetSerialzer


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
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        serializer = TodoViewSetSerialzer
        if self.action == 'create':
             serializer = TodoApiViewSetCreateSerializer

        return serializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        import pdb; pdb.set_trace()
        user_id = self.request.data.get('user_id', None)
        if user_id is not None:
            queryset =  queryset.filter(user__id=user_id)

        return queryset
