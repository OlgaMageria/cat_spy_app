# domain/exceptions/domain_exceptions.py

class DomainException(Exception):
    """Base domain exception"""
    pass

class CatNotFoundError(DomainException):
    """Raised when a cat is not found"""
    pass

class MissionNotFoundError(DomainException):
    """Raised when a mission is not found"""
    pass

class InvalidCatError(DomainException):
    """Raised when cat data is invalid"""
    pass

class InvalidMissionError(DomainException):
    """Raised when mission data is invalid"""
    pass

class CatAlreadyExistsError(DomainException):
    """Raised when trying to create a duplicate cat"""
    pass