#!/usr/bin/env python3
import unittest
from datetime import datetime
from models.user import User
from models import storage

class Teststorage(unittest.TestCase):

    def setUp(self):
        # Set up test data
        self.user_data = {
            "email": "test2@example.com",
            "hashed_password": "password123",
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": datetime(1990, 1, 1),
            "gender": "Male",
            "phone_number": "4234567890",
            "user_image_path": "/path/to/image.jpg",
            "user_video_path": "/path/to/video.mp4",
            "user_banner_path": "/path/to/banner.jpg",
            "is_admin": False,
            "is_active": True,
            "is_verified": False,
        }

    def test_db_storage_add(self):
        count = storage.count()

        # Create a user object
        user2 = User(**self.user_data)

        # Add the user to the storage
        storage.delete_all()
        storage.new(user2)
        storage.save()


        # Assert that the retrieved user matches the original data
        self.assertEqual(storage.count(), count + 1)

        # Clean up: Delete the user from the storage
        storage.delete(user2)
        storage.save()

        # Assert that the user was deleted
        self.assertEqual(storage.count(), count)