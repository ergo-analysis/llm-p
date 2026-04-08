class AppError(Exception):
    pass

class ConflictError(AppError):
    """Объект уже существует"""
    pass

class UnauthorizedError(AppError):
    """Неверные креды или неавторизован"""
    pass

class ForbiddenError(AppError):
    """Доступ запрещён"""
    pass

class NotFoundError(AppError):
    """объект не найден"""
    pass

class ExternalServiceError(AppError):
    """Ошибка пир обращении"""
    pass
