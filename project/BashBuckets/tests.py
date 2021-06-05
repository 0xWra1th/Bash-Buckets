from django.test import TestCase
import json

class Endpoints(TestCase):

    # Test that the index page is being served in response to GET
    def testIndexGET(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    # Test that the analytics page is being served in response to GET
    def testAnalyticsGET(self):
        response = self.client.get('/analytics')
        self.assertEqual(response.status_code, 200)

    # Test that the listFiles view is responding to POST
    def testListFilesPOST(self):
        data = {
            'token': 'ValidToken',
            'path': '/;nautilus',
            'bucket': 'testBucket',
        }
        response = self.client.post('/api/listFiles', json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    