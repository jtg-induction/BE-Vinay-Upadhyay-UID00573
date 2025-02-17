
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from projects import models as project_models
from users import models as user_models


class ProjectMemberAPITests(APITestCase):

    def setUp(self):
        self.user1 = user_models.CustomUser.objects.create(
            email='test1@gmail.com',
            first_name='test',
            last_name='user',
            password='somepassword'
        )
        self.user2 = user_models.CustomUser.objects.create(
            email='test2@gmail.com',
            first_name='test',
            last_name='user',
            password='somepassword'
        )
        self.user3 = user_models.CustomUser.objects.create(
            email='test3@gmail.com',
            first_name='test',
            last_name='user',
            password='somepassword'
        )
        self.project1 = project_models.Project.objects.create(
            name="TestProject1", max_members=2
        )
        self.project2 = project_models.Project.objects.create(
            name="TestProject2", max_members=3
        )
        self.project3 = project_models.Project.objects.create(
            name="TestProject3", max_members=4
        )
        self.url_add = reverse(
            'projects:projectmember', kwargs={'pk': self.project1.id, 'action': 'add'}
        )
        self.url_remove = reverse(
            'projects:projectmember', kwargs={'pk': self.project1.id, 'action': 'remove'}
        )

    def test_adding_members_to_project(self):
        response = self.client.patch(
            self.url_add,
            {'user_ids': [self.user2.id, self.user3.id]},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(project_models.ProjectMember.objects.filter(
            project=self.project1, member=self.user2).exists())
        self.assertTrue(project_models.ProjectMember.objects.filter(
            project=self.project1, member=self.user3).exists())
        self.assertEqual(
            response.data['log'][self.user2.id], 'added successfully')
        self.assertEqual(
            response.data['log'][self.user3.id], 'added successfully')

    def test_remove_users_from_project(self):
        project_models.ProjectMember.objects.create(
            project=self.project1, member=self.user1)
        project_models.ProjectMember.objects.create(
            project=self.project1, member=self.user2)
        response = self.client.patch(
            self.url_remove,
            {'user_ids': [self.user1.id, self.user2.id]},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(project_models.ProjectMember.objects.filter(
            project=self.project1, member=self.user1).exists())
        self.assertFalse(project_models.ProjectMember.objects.filter(
            project=self.project1, member=self.user2).exists())
        self.assertEqual(
            response.data['log'][self.user1.id], 'deleted successfully')
        self.assertEqual(
            response.data['log'][self.user2.id], 'deleted successfully')

    def test_addding_existing_member(self):
        project_models.ProjectMember.objects.create(
            project=self.project1, member=self.user1)
        response = self.client.patch(
            self.url_add,
            {'user_ids': [self.user1.id]},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['log'][self.user1.id], 'project_id already map to member_id')

    def test_user_already_in_two_projects(self):
        project_models.ProjectMember.objects.create(
            project=self.project2, member=self.user1)
        project_models.ProjectMember.objects.create(
            project=self.project3, member=self.user1)
        response = self.client.patch(
            self.url_add,
            {'user_ids': [self.user1.id]},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(project_models.ProjectMember.objects.filter(
            project=self.project1, member=self.user1).exists())
        self.assertEqual(response.data['log'][self.user1.id],
                         'User can\'t be part of more than two projects')

    def test_cannot_add_members_project_full(self):
        project_models.ProjectMember.objects.create(
            project=self.project1, member=self.user1)
        project_models.ProjectMember.objects.create(
            project=self.project1, member=self.user2)
        response = self.client.patch(
            self.url_add,
            {'user_ids': [self.user3.id]},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(project_models.ProjectMember.objects.filter(
            project=self.project1, member=self.user3).exists())
        self.assertEqual(response.data['log'][self.user3.id],
                         'Project member reach maximum limit')

    def test_cannot_remove_non_member(self):
        response = self.client.patch(
            self.url_remove,
            {'user_ids': [self.user1.id]},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['log'][self.user1.id], 'user is not a member')
    
