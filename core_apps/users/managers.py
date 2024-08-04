from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    # Method to validate the email address
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("You must provide a valid email address"))

    # Private method to handle user creation logic
    def _create_user(self, first_name, last_name, email, password, **extra_fields):
        # Ensure the required fields are provided
        if not first_name:
            raise ValueError(_("The user must have a first name."))
        if not last_name:
            raise ValueError(_("The user must have a last name."))
        if not email:
            raise ValueError(_("The user must have an email address."))

        # Normalize and validate the email
        email = self.normalize_email(email)
        self.email_validator(email)

        # Create the user model instance
        user = self.model(
            first_name=first_name, last_name=last_name, email=email, **extra_fields
        )
        # Set the user's password
        user.set_password(password)
        # Save the user to the database
        user.save(using=self._db)
        return user

    # Method to create a regular user
    def create_user(self, first_name, last_name, email, password=None, **extra_fields):
        # Set default values for regular users
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        # Use the private method to create the user
        return self._create_user(first_name, last_name, email, password, **extra_fields)

    # Method to create a superuser
    def create_superuser(
        self, first_name, last_name, email, password=None, **extra_fields
    ):
        # Set default values for superusers
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        # Ensure the required fields for superusers are correctly set
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        if not password:
            raise ValueError(_("Superuser must have a password."))

        # Use the private method to create the superuser
        return self._create_user(first_name, last_name, email, password, **extra_fields)
