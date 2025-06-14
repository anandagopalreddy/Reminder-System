import unittest
import requests
from datetime import datetime, timedelta


class TestAPI(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:8000"

    def test_create_user(self):
        url = f"{self.BASE_URL}/create-user"
        payload = {"username": "testuser", "email": "testuser@example.com"}
        response = requests.post(url, json=payload)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertIn("user_id", response_data)
        self.assertEqual(response_data["message"], "User created successfully.")

    def test_create_reminder(self):
        url = f"{self.BASE_URL}/create-reminder"
        payload = {
            "user_id": 1,
            "message": "Test reminder",
            "weeks": 1,
            "days": 0,
            "hours": 0,
            "minutes": 0
        }
        response = requests.post(url, json=payload)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertIn("Total Wait Time", response_data["data"])
        self.assertIn("Scheduled Time", response_data["data"])

    def test_calculate_snooze_time(self):
        url = f"{self.BASE_URL}/calculate-snooze-time"
        payload = {
            "reminder_id": 1,
            "weeks": 0,
            "days": 1,
            "hours": 2,
            "minutes": 30
        }
        response = requests.post(url, json=payload)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("Total Wait Time", response_data["data"])
        self.assertIn("New Scheduled Time", response_data["data"])

    def test_update_reminder(self):
        url = f"{self.BASE_URL}/update-reminder"
        payload = {
            "reminder_id": 1,
            "weeks": 0,
            "days": 2,
            "hours": 3,
            "minutes": 0
        }
        response = requests.post(url, json=payload)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("Total Wait Time", response_data["data"])
        self.assertIn("Scheduled Time", response_data["data"])

    def test_update_reminder_no_snooze(self):
        url = f"{self.BASE_URL}/update-reminder"
        payload = {
            "reminder_id": 1,
            "weeks": 0,
            "days": 0,
            "hours": 0,
            "minutes": 0
        }
        response = requests.post(url, json=payload)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["data"]["status"], "REMINDER_DELETED")
        self.assertIn("Scheduled Time", response_data["data"])

if __name__ == "__main__":
    unittest.main()
