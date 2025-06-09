from django.test import TestCase
from django.db import IntegrityError
from .models import SecureCipherUser


class SecureCipherUserModelTest(TestCase):
    
    def setUp(self):
        """What it does: Sets up test data that will be used across multiple test methods"""
        self.valid_user_data = {
            'username': 'testuser',
            'full_name': 'Test User',
            'email': 'test@example.com',
            'phone_number': '08012345678',
            'bvn': '12345678901',
            'nin': '98765432101',
            'ecdsa_public_key': 'test_public_key_data'
        }

    def test_user_creation_with_valid_data(self):
        """What it does: Tests that a user can be created with valid data"""
        user = SecureCipherUser.objects.create(**self.valid_user_data)
        
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.full_name, 'Test User')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.phone_number, '08012345678')
        self.assertEqual(user.bvn, '12345678901')
        self.assertEqual(user.nin, '98765432101')
        self.assertEqual(user.ecdsa_public_key, 'test_public_key_data')
        self.assertIsNotNone(user.registered_at)

    def test_virtual_account_id_generation_with_leading_zero(self):
        """What it does: Tests that virtual account ID is generated correctly with phone numbers starting with 0"""
        user = SecureCipherUser.objects.create(**self.valid_user_data)
        
        # What it does: Should strip leading 0 and add VX- prefix
        expected_account_id = "VX-8012345678"
        self.assertEqual(user.virtual_account_id, expected_account_id)

    def test_virtual_account_id_generation_without_leading_zero(self):
        """What it does: Tests virtual account ID generation with phone numbers not starting with 0"""
        self.valid_user_data['phone_number'] = '7012345678'
        user = SecureCipherUser.objects.create(**self.valid_user_data)
        
        # What it does: Should add VX- prefix without stripping anything
        expected_account_id = "VX-7012345678"
        self.assertEqual(user.virtual_account_id, expected_account_id)

    def test_virtual_account_id_not_overwritten_if_exists(self):
        """What it does: Tests that existing virtual_account_id is not overwritten"""
        self.valid_user_data['virtual_account_id'] = 'VX-CUSTOM123'
        user = SecureCipherUser.objects.create(**self.valid_user_data)
        
        # What it does: Should keep the custom virtual account ID
        self.assertEqual(user.virtual_account_id, 'VX-CUSTOM123')

    def test_username_uniqueness(self):
        """What it does: Tests that usernames must be unique"""
        SecureCipherUser.objects.create(**self.valid_user_data)
        
        # What it does: Attempting to create another user with same username should fail
        duplicate_data = self.valid_user_data.copy()
        duplicate_data['email'] = 'different@example.com'
        duplicate_data['phone_number'] = '08087654321'
        duplicate_data['bvn'] = '10987654321'
        duplicate_data['nin'] = '12345678909'
        
        with self.assertRaises(IntegrityError):
            SecureCipherUser.objects.create(**duplicate_data)

    def test_email_uniqueness(self):
        """What it does: Tests that emails must be unique"""
        SecureCipherUser.objects.create(**self.valid_user_data)
        
        # What it does: Attempting to create another user with same email should fail
        duplicate_data = self.valid_user_data.copy()
        duplicate_data['username'] = 'differentuser'
        duplicate_data['phone_number'] = '08087654321'
        duplicate_data['bvn'] = '10987654321'
        duplicate_data['nin'] = '12345678909'
        
        with self.assertRaises(IntegrityError):
            SecureCipherUser.objects.create(**duplicate_data)

    def test_phone_number_uniqueness(self):
        """What it does: Tests that phone numbers must be unique"""
        SecureCipherUser.objects.create(**self.valid_user_data)
        
        # What it does: Attempting to create another user with same phone number should fail
        duplicate_data = self.valid_user_data.copy()
        duplicate_data['username'] = 'differentuser'
        duplicate_data['email'] = 'different@example.com'
        duplicate_data['bvn'] = '10987654321'
        duplicate_data['nin'] = '12345678909'
        
        with self.assertRaises(IntegrityError):
            SecureCipherUser.objects.create(**duplicate_data)

    def test_bvn_uniqueness(self):
        """What it does: Tests that BVNs must be unique"""
        SecureCipherUser.objects.create(**self.valid_user_data)
        
        # What it does: Attempting to create another user with same BVN should fail
        duplicate_data = self.valid_user_data.copy()
        duplicate_data['username'] = 'differentuser'
        duplicate_data['email'] = 'different@example.com'
        duplicate_data['phone_number'] = '08087654321'
        duplicate_data['nin'] = '12345678909'
        
        with self.assertRaises(IntegrityError):
            SecureCipherUser.objects.create(**duplicate_data)

    def test_nin_uniqueness(self):
        """What it does: Tests that NIINs must be unique"""
        SecureCipherUser.objects.create(**self.valid_user_data)
        
        # What it does: Attempting to create another user with same NIN should fail
        duplicate_data = self.valid_user_data.copy()
        duplicate_data['username'] = 'differentuser'
        duplicate_data['email'] = 'different@example.com'
        duplicate_data['phone_number'] = '08087654321'
        duplicate_data['bvn'] = '10987654321'
        
        with self.assertRaises(IntegrityError):
            SecureCipherUser.objects.create(**duplicate_data)

    def test_virtual_account_id_uniqueness(self):
        """What it does: Tests that virtual account IDs must be unique"""
        SecureCipherUser.objects.create(**self.valid_user_data)
        
        # What it does: Attempting to create another user with same phone (same virtual account ID) should fail
        duplicate_data = self.valid_user_data.copy()
        duplicate_data['username'] = 'differentuser'
        duplicate_data['email'] = 'different@example.com'
        duplicate_data['bvn'] = '10987654321'
        duplicate_data['nin'] = '12345678909'
        # Same phone number will generate same virtual_account_id
        
        with self.assertRaises(IntegrityError):
            SecureCipherUser.objects.create(**duplicate_data)

    def test_string_representation(self):
        """What it does: Tests the __str__ method returns correct format"""
        user = SecureCipherUser.objects.create(**self.valid_user_data)
        expected_str = f"testuser (VX-8012345678)"
        self.assertEqual(str(user), expected_str)

    def test_registered_at_auto_populated(self):
        """What it does: Tests that registered_at timestamp is automatically set"""
        user = SecureCipherUser.objects.create(**self.valid_user_data)
        self.assertIsNotNone(user.registered_at)

    def test_multiple_leading_zeros_stripped(self):
        """What it does: Tests that multiple leading zeros are properly stripped"""
        self.valid_user_data['phone_number'] = '00012345678'
        user = SecureCipherUser.objects.create(**self.valid_user_data)
        
        # What it does: Should strip all leading zeros
        expected_account_id = "VX-12345678"
        self.assertEqual(user.virtual_account_id, expected_account_id)

    def test_phone_number_with_no_digits_after_stripping(self):
        """What it does: Tests edge case where phone number is all zeros"""
        self.valid_user_data['phone_number'] = '00000000000'
        user = SecureCipherUser.objects.create(**self.valid_user_data)
        
        # What it does: Should result in VX- prefix only (edge case)
        expected_account_id = "VX-"
        self.assertEqual(user.virtual_account_id, expected_account_id)