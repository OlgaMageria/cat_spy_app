# domain/services/cat_domain_service.py
from typing import Optional
from domain.entities.cat import Cat
from domain.repositories.cat_repository import CatRepository

class CatDomainService:
    """Service for cat-related domain operations"""
    
    def __init__(self, cat_repository: CatRepository):
        self.cat_repository = cat_repository
    
    def authenticate_cat(self, email: str, password: str) -> Optional[Cat]:
        """Authenticate a cat with email and password"""
        cat = self.cat_repository.find_by_email(email)
        if cat and cat.verify_password(password):
            return cat
        return None
    
    def cat_with_email_exists(self, email: str) -> bool:
        """Check if a cat with given email already exists"""
        return self.cat_repository.find_by_email(email) is not None