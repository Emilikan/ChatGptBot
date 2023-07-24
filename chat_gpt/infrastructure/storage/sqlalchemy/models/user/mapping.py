from .user import user_mapping as user_mapping_
from .user_context import user_context_mapping


def user_mapping():
    user_mapping_()
    user_context_mapping()
