import requests
import os

BASE_URL = "http://localhost:8000/api/"

class APIClient:
    def __init__(self):
        self.token = None

    def login(self, username, password):
        try:
            url = f"{BASE_URL}token/"
            # Ensure no existing auth header interferes with login
            response = requests.post(url, data={'username': username, 'password': password})
            response.raise_for_status()
            data = response.json()
            self.token = data['access']
            return True
        except Exception as e:
            print(f"Login failed: {e}")
            return False

    def _get_headers(self):
        headers = {}
        if self.token:
            headers['Authorization'] = f"Bearer {self.token}"
        return headers

    def upload_dataset(self, file_path):
        url = f"{BASE_URL}upload/"
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(url, files=files, headers=self._get_headers())
                response.raise_for_status()
                return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Upload failed: {e}")
            raise

    def get_history(self):
        url = f"{BASE_URL}history/"
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Fetch history failed: {e}")
            return []

    def get_summary(self, dataset_id):
        url = f"{BASE_URL}summary/{dataset_id}/"
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Fetch summary failed: {e}")
            raise

    def delete_dataset(self, dataset_id):
        url = f"{BASE_URL}summary/{dataset_id}/"
        try:
            response = requests.delete(url, headers=self._get_headers())
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Delete failed: {e}")
            return False
