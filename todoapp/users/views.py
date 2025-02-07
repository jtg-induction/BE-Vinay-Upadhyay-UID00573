from django.contrib.auth import authenticate
from rest_framework import generics, permissions, response, views
from rest_framework.authtoken.models import Token

from .models import CustomUser
from .serializers import UserRegistrationSerializer


class UserRegistrationAPIView(generics.CreateAPIView, generics.GenericAPIView):
    """
        success response format
         {
           first_name: "",
           last_name: "",
           email: "",
           date_joined: "",
           "token"
         }
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serialized_data = self.get_serializer(data=request.data)
        if not serialized_data.is_valid():
            return response.Response(serialized_data.errors)
        data = serialized_data.validated_data
        user = CustomUser.objects.create_user(**data)
        token, created = Token.objects.get_or_create(user=user)
        data["token"] = token.key

        return  response.Response(data)

             
class UserLoginAPIView(views.APIView):
    """
        success response format
         {
           auth_token: ""
         }
    """
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        user = authenticate(username=request.data['email'], password=request.data['password'])
        respons = response.Response({'error' : 'Invalid credentials'}, status=401)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            respons = response.Response({'token': token.key})
      
        return respons
        