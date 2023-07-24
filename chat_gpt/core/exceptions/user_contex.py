from .base import CoreException


class UserContextAlreadyExistsException(CoreException):
    ...


class UserContextNotFoundException(CoreException):
    ...


class MoreUserContextsFoundException(CoreException):
    ...
