# Typing
from typing import List, Optional, Union, Tuple

# Django
from django.db.models.query import QuerySet
from numpy import product

# Models (Users)
from icard.apps.users.models import User

# Lib
from icard.apps.users.lib.exceptions import CantCreateUser, CantUpdateUserStatus, UserDoesNotExist, GroupDoesNotExist


from icard.apps.users.providers import group as group_providers

from datetime import datetime


def get_user_by_pk(pk: int) -> Optional[User]:
    """
    Method to obtain a user by pk
    - Returns: Optional[User]
    """
    try:
        user = User.objects.get(pk=pk)
        return user
    except User.DoesNotExist:
        return None


def get_user_by_identification_number(identification_number: str) -> Optional[User]:
    """
    Method to obtain a user by identification_number
    - Returns_ Optional[User]
    """
    try:
        user = User.objects.get(identification_number=identification_number)
        return user
    except User.DoesNotExist:
        return None


def get_user_by_email(email: str) -> Optional[User]:
    """
    Method to obtain a user by email
    - Returns_ Optional[User]
    """
    try:
        user = User.objects.get(email=email)
        return user
    except User.DoesNotExist:
        return None


def get_active_users() -> Union[QuerySet, List[User]]:
    """
    Method for get active users 
    - Returns: List[Users]
    """
    users = User.objects.filter(is_active=True).order_by("first_name")
    return users


def create_user(
    first_name: str,
    last_name: str,
    identification_number: str,
    email: str,
    phone_number: str,
    ip_address: str,
    password: str
) -> Optional[User]:
    """
    Method for create user
    - Returns: Optional[User]
    """
    try:
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            identification_number=identification_number,
            email=email,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save()
        add_ip_address_by_user(user=user, ip_address=ip_address)
        add_group_to_user(user=user, group_name="customer")
        return user
    except CantCreateUser:
        return None


def add_ip_address_by_user(user: User, ip_address: str) -> None:
    if not user.ip_address.get(ip_address):
        user.ip_address[ip_address] = str(datetime.now())
        user.save(update_fields=["ip_address", "updated_at"])


def get_all_users() -> Union[QuerySet, List[User]]:
    users = User.objects.all()
    return users


def add_group_to_user(user: User, group_name: str) -> None:
    try:
        group = group_providers.get_group_by_name(name=group_name)
        user.groups.add(group)
    except (User.DoesNotExist, GroupDoesNotExist):
        return None


def update_user_by_pk(user_pk: int, **kwargs) -> Optional[User]:
    """
    Method for update user by pk
    - Returns: Optional[User]    
    """
    try:
        user = get_user_by_pk(pk=user_pk)
        update_fields = ["updated_at"]
        for key, value in kwargs.items():
            setattr(user, key, value if callable(value) else value)
            update_fields.append(key)
        user.save(update_fields=update_fields)
        return user
    except User.DoesNotExist:
        return None


def check_user_is_owner_or_staff(request_user: "users.User", user_pk: int) -> bool:
    """
    Method to botain user authorized or staff
    """
    if int(request_user.pk) == user_pk:
        return True
    return request_user.is_staff
