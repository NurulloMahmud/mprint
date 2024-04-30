from django.contrib.auth.models import AbstractUser
from django.db import models

from main.models import Branch


class CustomUser(AbstractUser):
    ADMIN = 'admin'
    PECHAT = 'pechat'
    SEX = 'sex'
    MANAGER = 'manager'
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (PECHAT, 'Pechat'),
        (SEX, 'Sex'),
        (MANAGER, 'Manager'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=None,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=False)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)

    # Adding related_name to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="customuser_set",
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_set",
        related_query_name="customuser",
    )
