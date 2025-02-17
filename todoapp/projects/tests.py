from rest_framework.test import APITestCase
from django.urls import reverse

from users.models import CustomUser
from projects.models import Project


class ProjectAPITest(APITestCase):

    def setUp(self):
        self.user1 = CustomUser.objects.create(email="user1@gmail.com", password="user@123",
                                              first_name="John", last_name="Dio")
        self.user2 = CustomUser.objects.create(email="user2@gmail.com", password="user@123",
                                              first_name="John", last_name="Dio")
        self.user3 = CustomUser.objects.create(email="user3@gmail.com", password="user@123",
                                               first_name="John", last_name="Dio")
        self.user4 = CustomUser.objects.create(email="user4@gmail.com", password="user@123",
                                               first_name="John", last_name="Dio")
        self.project1 = Project.objects.create(name="project1", max_members=3)
        self.project2 = Project.objects.create(name="project2", max_members=3)
        self.project3 = Project.objects.create(name="project3", max_members=3)
        
    
    def test_add_member(self):
        pk = self.project1.id
        action = 'add'

        url = reverse('projects:projectmember', args=[pk, action])

        data = {
            "uids" : [self.user1.id]
        }
        
        response = self.client.patch(url, data, HTTP_AUTHORISATION=f'Token {self.token.key}', format='json')
        
        self.assertEqual(response.status_code, self.HTTP_200_OK)
    
    def test_remove_member(self):
        pk  = self.project1.id
        action = 'remove'

        url = reverse('projects:projectmember', args=[pk, action])

        data = {
            'user_ids' : [self.user1.id]
        }

        response = self.client.patch(url, data, HTTP_AUTHORISATION=f'Token {self.token.key}', format='json')

        self.assertEqual(response.status_code, self.HTTP_200_OK)
        

    
