from fastapi import status


class BadRequestException(Exception):
    def __init__(
        self, error_code: str, message: str = None, debug_info: str = None
    ) -> None:
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.error_code = error_code
        self.message = message
        self.debug_info = debug_info


class UnauthorizedException(Exception):
    def __init__(
        self, error_code: str, message: str = None, debug_info: str = None
    ) -> None:
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.error_code = error_code
        self.message = message
        self.debug_info = debug_info


class AccessDeniedException(Exception):
    def __init__(
        self, error_code: str, message: str = None, debug_info: str = None
    ) -> None:
        self.status_code = status.HTTP_403_FORBIDDEN
        self.error_code = error_code
        self.message = message
        self.debug_info = debug_info


class ErrorCode:
    ERR_UNAUTHORIZED = "ERR_UNAUTHORIZED"
    ERR_ACCESS_DENIED = "ERR_ACCESS_DENIED"
    ERR_INTERNAL_SERVER_ERROR = "ERR_INTERNAL_SERVER_ERROR"
    ERR_USER_EXISTED = "ERR_USER_EXISTED"
    ERR_TOKEN_EXPIRED = "ERR_TOKEN_EXPIRED"
    ERR_WORD_NOT_FOUND = "ERR_WORD_NOT_FOUND"
    ERR_LESSON_NOT_EDITABLE = "ERR_LESSON_NOT_EDITABLE"

    ERR_GROUP_EXISTED = "ERR_GROUP_EXISTED"
    ERR_PROGRESS_NOT_FOUND = "ERR_PROGRESS_NOT_FOUND"
    ERR_PROGRESS_WORD_NOT_FOUND = "ERR_PROGRESS_WORD_NOT_FOUND"
    ERR_PROGRESS_SENTENCE_NOT_FOUND = "ERR_PROGRESS_SENTENCE_NOT_FOUND"
    ERR_GROUP_NOT_FOUND = "ERR_GROUP_NOT_FOUND"
    ERR_USER_ALREADY_JOINED_GROUP = "ERR_USER_ALREADY_JOINED_GROUP"

    ERR_GROUP_MEMBER_NOT_FOUND = "ERR_GROUP_MEMBER_NOT_FOUND"
    ERR_USER_NOT_MANAGER = "ERR_USER_NOT_MANAGER"

    ERR_INVALID_TOKEN = "ERR_INVALID_TOKEN"


class ErrorMessage:
    ERR_UNAUTHORIZED = "You are not authorized"
    ERR_ACCESS_DENIED = "You can not access"
    ERR_INTERNAL_SERVER_ERROR = "Server error"
    ERR_USER_EXISTED = "This user is existed"
    ERR_WORD_NOT_FOUND = "Word not found"
    ERR_GROUP_EXISTED = "Group is already existed"
    ERR_PROGRESS_NOT_FOUND = "Progress not found"
    ERR_PROGRESS_WORD_NOT_FOUND = "Progress word not found"
    ERR_PROGRESS_SENTENCE_NOT_FOUND = "Progress sentence not found"
    ERR_LESSON_NOT_EDITABLE = "Lesson is not editable"
    ERR_GROUP_NOT_FOUND = "Group not found"
    ERR_USER_ALREADY_JOINED_GROUP = "User already joined group"
    ERR_GROUP_MEMBER_NOT_FOUND = "Group member not found"
    ERR_USER_NOT_MANAGER = "User is not manager"
    ERR_INVALID_TOKEN = "Invalid token"
