from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Task


class TestAPI(APITestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user('user', 'user@user.com', 'useruser')
        self.user2 = get_user_model().objects.create_user('user2', 'user2@user.com', 'useruser')
        manager = Group.objects.create(name='manager')
        manager.user_set.add(self.user)

    def test_task_CRUD(self):
        url = reverse('api:tasks-list')
        data = {
            "title": "1",
            "description": "asdvasdvasdv",
            "start_time": "2021-07-06T12:25:56Z",
            "end_time": "2021-07-06T13:24:23Z",
            "user": 2
        }
        wrong_data_1 = {
            "title": "wrong",
            "description": "asdvasdvasdvlyil",
            "start_time": "2021-07-06T12:40:56Z",
            "end_time": "2021-07-06T13:10:23Z",
            "user": 2
        }
        wrong_data_2 = {
            "title": "wrong",
            "description": "asdvasdvasdvlyil",
            "start_time": "2021-07-06T11:40:56Z",
            "end_time": "2021-07-06T12:30:23Z",
            "user": 2
        }
        wrong_data_3 = {
            "title": "wrong",
            "description": "asdvasdvasdvlyil",
            "start_time": "2021-07-06T12:40:56Z",
            "end_time": "2021-07-06T13:20:23Z",
            "user": 2
        }
        wrong_data_4 = {
            "title": "wrong",
            "description": "asdvasdvasdvlyil",
            "start_time": "2021-07-06T7:40:56Z",
            "end_time": "2021-07-06T15:20:23Z",
            "user": 2
        }
        """Unauthorized user can't post data"""
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        """User in manager group can create tasks"""
        self.client.login(username='user', password='useruser')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.user.groups.filter(name='manager').values('name')[0]['name'], 'manager')
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, '1')
        """validation check"""
        response = self.client.post(url, wrong_data_1, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Task.objects.count(), 1)
        response = self.client.post(url, wrong_data_2, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Task.objects.count(), 1)
        response = self.client.post(url, wrong_data_3, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Task.objects.count(), 1)
        response = self.client.post(url, wrong_data_4, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Task.objects.count(), 1)
        self.client.logout()
        """Simple user can't create tasks"""
        self.client.login(username='user2', password='useruser')
        data2 = {
            "title": "2",
            "description": "asdvasdvasdv",
            "start_time": "2021-07-06T12:25:56Z",
            "end_time": "2021-07-06T13:24:23Z",
            "user": 2
        }
        response = self.client.post(url, data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Task.objects.filter(user_id=self.user2.id).count(), 1)
        """Simple user can update tasks"""
        url_detail = reverse('api:tasks-detail', kwargs={'pk': Task.objects.get(title=data['title']).pk})
        data_upd = {
            "title": '1_updated'
        }
        response = self.client.patch(url_detail, data_upd, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(Task.objects.get().title, '1_updated')
        """Simple user can't delete tasks"""
        response = self.client.delete(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data)
        self.assertEqual(Task.objects.count(), 1)
        self.client.logout()
        """Manager can update tasks"""
        self.client.login(username='user', password='useruser')
        data_upd_by_manager = {
            "stage": 'InD'
        }
        response = self.client.patch(url_detail, data_upd_by_manager, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(Task.objects.get().title, '1_updated')
        self.assertEqual(Task.objects.get().stage, 'InD')
        """Manager can delete tasks"""
        response = self.client.delete(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, msg=response.data)
        self.assertEqual(Task.objects.count(), 0)