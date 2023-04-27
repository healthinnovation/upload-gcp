import os
import unittest
from unittest import mock
from unittest.mock import patch, Mock, MagicMock
from google.cloud.storage.blob import Blob
from google.cloud.storage.bucket import Bucket
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

from src.upload_to_gcs import upload_file_to_gcs

class TestUploadToGCS(unittest.TestCase):
    
    def setUp(self):
        self.bucket_name = 'test-bucket'
        self.directory = 'tests/data'
        self.test_files = ['test_1.txt', 'test_2.txt', 'test_3.txt']
        self.credentials = Credentials.from_service_account_file('path/to/credentials.json')
        self.credentials = self.credentials.with_scopes(['https://www.googleapis.com/auth/cloud-platform'])
        self.client = MagicMock()
        self.bucket = MagicMock(spec=Bucket)
        self.blob = MagicMock(spec=Blob)
        self.blob.create_resumable_upload_session.return_value = {'session_url': 'http://test.com/upload'}
        self.client.bucket.return_value = self.bucket
        self.bucket.get_blob.return_value = self.blob
        self.request = MagicMock(spec=Request)
        self.request.run.return_value.status_code = 200
        
    @patch('builtins.open', new_callable=mock.mock_open, read_data=b'Test data')
    def test_upload_file_to_gcs(self, mock_open):
        self.assertTrue(upload_file_to_gcs(self.test_files[0], self.client, self.bucket_name, self.directory, self.credentials, self.request))
        self.blob.create_resumable_upload_session.assert_called_once()
        self.request.run.assert_called()
        self.assertEqual(self.request.run.call_count, 2)
        self.bucket.blob.assert_called_once_with(self.test_files[0])
        
    def test_upload_file_to_gcs_raises_exception(self):
        self.request.run.return_value.status_code = 500
        self.assertFalse(upload_file_to_gcs(self.test_files[0], self.client, self.bucket_name, self.directory, self.credentials, self.request))
        
    def test_upload_file_to_gcs_returns_false_on_exception(self):
        self.blob.create_resumable_upload_session.side_effect = Exception('Error creating session')
        self.assertFalse(upload_file_to_gcs(self.test_files[0], self.client, self.bucket_name, self.directory, self.credentials, self.request))
        
    def test_upload_file_to_gcs_skips_previously_uploaded_files(self):
        self.bucket.get_blob.return_value.download_as_text.return_value = 'test_2.txt'
        self.assertTrue(upload_file_to_gcs(self.test_files[2], self.client, self.bucket_name, self.directory, self.credentials, self.request))
        self.assertEqual(self.bucket.get_blob.call_count, 1)
        self.assertEqual(self.bucket.blob.call_count, 0)
        
if __name__ == '__main__':
    unittest.main()
