class CantCreateUser(BaseException):
    pass


class CantUpdateUser(BaseException):
    pass


class CantUpdateUserStatus(CantUpdateUser):
    pass


class UserDoesNotExist(BaseException):
    pass


class GroupDoesNotExist(BaseException):
    pass
