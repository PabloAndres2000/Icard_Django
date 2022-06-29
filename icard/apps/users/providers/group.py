from tokenize import group
from typing import Optional

from django.contrib.auth.models import Group


def get_group_by_name(name: str) -> Optional[Group]:
    """
    Method to get groupd by name
    - Returns:  Optional[Group]
    """
    try:
        group = Group.objects.get(name=name)
        return group
    except Group.DoesNotExist:
        return None
