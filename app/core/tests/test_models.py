from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

def sample_user(email='rsreddy@gmail.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)

class ModelTest(TestCase):

    def test_create_user_with_email_successful(self):
        """test creating a user with an email is sucessuful"""
        email = "testuser@gmail.com"
        password = "testpassword"
        user = get_user_model().objects.create_user(
             email=email,
             password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normailize(self):
        """test the email for a new user is normalize"""
        email = 'testuser@GMAIL.COM'
        user = get_user_model().objects.create_user(email, "testpassword")

        self.assertEqual(user.email, email.lower())

    def test_new_user_email_invalid(self):
        """test creating user with no email raise error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "testpassword")

    def test_new_super_user_create(self):
        '''Test creating a superuser'''
        user = get_user_model().objects.create_superuser(
             "srinath@gmail.com",
             'testpassword'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
           user=sample_user(),
           name='Vegan'
        )
        self.assertEqual(str(tag), tag.name)

    def test_inge_str(self):
        ingredient = models.Ingredient.objects.create(
           user=sample_user(),
           name="cucumber"
        )
        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """TEst the recipe string representation"""
        recipe = models.Recipe.objects.create(
             user=sample_user(),
             title="Steak and mushroom sauce",
             time_minutes=5,
             price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)
