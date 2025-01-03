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
    ERR_UNAUTHORIZED = "Bạn không có quyền truy cập"
    ERR_ACCESS_DENIED = "Bạn không thể truy cập"
    ERR_INTERNAL_SERVER_ERROR = "Lỗi máy chủ"
    ERR_USER_EXISTED = "Người dùng này đã tồn tại"
    ERR_WORD_NOT_FOUND = "Không tìm thấy từ"
    ERR_GROUP_EXISTED = "Nhóm đã tồn tại"
    ERR_PROGRESS_NOT_FOUND = "Không tìm thấy tiến trình"
    ERR_PROGRESS_WORD_NOT_FOUND = "Không tìm thấy từ trong tiến trình"
    ERR_PROGRESS_SENTENCE_NOT_FOUND = "Không tìm thấy câu trong tiến trình"
    ERR_LESSON_NOT_EDITABLE = "Bài học không thể chỉnh sửa"
    ERR_GROUP_NOT_FOUND = "Không tìm thấy nhóm"
    ERR_USER_ALREADY_JOINED_GROUP = "Người dùng đã tham gia nhóm"
    ERR_GROUP_MEMBER_NOT_FOUND = "Không tìm thấy thành viên nhóm"
    ERR_USER_NOT_MANAGER = "Người dùng không phải là quản lý"
    ERR_INVALID_TOKEN = "Token không hợp lệ"
