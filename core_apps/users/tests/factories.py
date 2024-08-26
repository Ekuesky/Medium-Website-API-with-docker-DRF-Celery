# Imports for creating fake user objects for testing
import factory
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from faker import Factory as FakerFactory

# Create a Faker instance for generating random data
faker = FakerFactory.create()

# Get the User model from Django
User = get_user_model()


# Temporarily disable post_save signal during user creation (avoids infinite loop)
@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory class to create fake user objects for testing.

    This class inherits from factory.django.DjangoModelFactory and defines attributes
    for first_name, last_name, email, password, is_active, and is_staff using Faker.

    The _create method overrides the default behavior and handles creating both
    regular users and superusers based on the presence of the "is_superuser" keyword argument.
    """

    class Meta:
        model = User  # Specify the model this factory creates objects for

    first_name = factory.LazyAttribute(lambda x: faker.first_name())
    last_name = factory.LazyAttribute(lambda x: faker.last_name())
    email = factory.LazyAttribute(lambda x: faker.email())
    password = factory.LazyAttribute(lambda x: faker.password())
    is_active = True
    is_staff = False

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """
        Overrides default _create method to handle superuser creation.

        This method checks for the "is_superuser" argument. If present, it uses
        create_superuser, otherwise it uses create_user from the User manager.
        """
        manager = cls._get_manager(
            model_class
        )  # Get the manager instance from the model class
        if "is_superuser" in kwargs:
            return manager.create_superuser(*args, **kwargs)
        else:
            return manager.create_user(*args, **kwargs)
