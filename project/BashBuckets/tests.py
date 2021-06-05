from django.test import TestCase

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
            'path': '/',
            'bucket': 'myBucket',
        }
        response = self.client.post('/api/listFiles',params=data)
        self.assertEqual(response.status_code, 200)

    