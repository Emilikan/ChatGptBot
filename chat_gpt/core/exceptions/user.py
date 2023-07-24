from .base import CoreException


class UserAlreadyExistsException(CoreException):
    ...


class UserNotFoundException(CoreException):
    ...


class MoreUsersFoundException(CoreException):
    ...
