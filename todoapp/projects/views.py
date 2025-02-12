from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Q

from users.models import CustomUser

from .serializers import ProjectMemberSerializer
from .models import Project, ProjectMember


class ProjectMemberApiViewSet(APIView):
    """
       constraints
        - a user can be a member of max 2 projects only
        - a project can have at max N members defined in database for each project
       functionalities
       - add users to projects

         Request
         { user_ids: [1,2,...n] }
         Response
         {
           logs: {
             <user_id>: <status messages>
           }
         }
         following are the possible status messages
         case1: if user is added successfully then - "Member added Successfully"
         case2: if user is already a member then - "User is already a Member"
         case3: if user is already added to 2 projects - "Cannot add as User is a member in two projects"

         there will be many other cases think of that

       - update to remove users from projects

         Request
         { user_ids: [1,2,...n] }

         Response
         {
           logs: {
             <user_id>: <status messages>
           }
         }

         there will be many other cases think of that and share on forum
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
           user_ids =  request.data.get('user_ids', [])
           project_id = request.query_params.get('project_id')
           project_details = Project.objects.filter(id=int(project_id))
           projects_max_members = project_details[0].max_members
           bulk_create_data = []
           output_log = {}

           for user_id in user_ids:
                projects_user_count = project_details.values('members').count()

                if projects_user_count < projects_max_members:
                      users_project_counts =   ProjectMember.objects.filter(member_id=user_id).values("project").distinct().count()

                      if users_project_counts < 2 : 
                          serialized_data = ProjectMemberSerializer(data = {
                           'member_id' : user_id,
                           'project_id' : project_id
                          }) 

                          if not serialized_data.is_valid():
                            print("invalid")
                            print(serialized_data.errors) 
                            output_log[user_id] = {'message' : 'not successfully attached'}
                            continue;
                          
                          obj = ProjectMember(**serialized_data.validated_data)
                          bulk_create_data.append(obj)  
                          output_log[user_id] = {'message' : 'successully added'}
                      else:
                          output_log[user_id] = {'message' : 'not successfully attached'}

                else:
                     output_log[user_id] = {'message' : 'not successfully attached'}
          
           ProjectMember.objects.bulk_create(bulk_create_data)
           print(output_log)

           return Response(output_log)
    
    def delete(self, request, *args, **kwargs):
         user_ids = request.data.get('user_ids', [])
         project_id = request.query_params.get('project_id')
         output_log = {}

         for user_id in user_ids:
              
              serialized_data = ProjectMemberSerializer(data={
                  'project_id': int(project_id),
                  'member_id': user_id
              })
              x = serialized_data.is_valid()
              print(serialized_data.data)

              if not x:
                   print(serialized_data.error)
                   output_log[user_id] = {'message' : 'invalid credentials can not be deleted'}
                   continue
              
              ProjectMember.objects.filter(Q(project=int(project_id)) & Q(member=user_id)).delete()
              output_log[user_id] = {'message' : 'successfully deleted'}

         return Response(output_log)
