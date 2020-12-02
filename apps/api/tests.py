from django.test import TestCase

from django.contrib.auth.models import User
from apps.api.serializers import CategorySerializer


class BaseModelTest(TestCase):
    fixtures = ['test_user_data']

    def test_user(self):
        user = User.objects.first()
        self.assertIsNotNone(user)


class CategoryTest(TestCase):
    fixtures = ['test_user_data', 'test_category_data']

    def setUp(self) -> None:  # noqa
        self.user: User = User.objects.first()

    def test_create_category(self):
        serializer = CategorySerializer(
            data=dict(
                name='demo',
                display_name='demo',
                created_by=self.user.id
            )
        )
        serializer.is_valid(raise_exception=True)
        category = serializer.save()
        self.assertIsNotNone(category)
        self.assertEqual(category.created_by, self.user)
        self.assertEqual(category.modified_by, self.user)
        self.assertEqual(category.owned_by, self.user)

    def test_detail_category(self):
        pass
