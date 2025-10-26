from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from domain.value_objects.email import Email
from domain.value_objects.password import Password
from domain.value_objects.breed import Breed
from domain.value_objects.salary import Salary

@dataclass
class Cat:
    """Cat aggregate root"""
    uuid: UUID
    name: str
    breed: Breed
    email: Email
    password: Password
    salary: Salary
    is_admin: bool = False
    created_at: datetime = field(default_factory=datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=datetime.now(timezone.utc))
    
    @classmethod
    def create(cls, name: str, breed: Breed, email: Email, 
               password: Password, salary: Salary) -> "Cat":
        """Factory method to create a new Cat"""
        return cls(
            uuid=uuid4(),
            name=name,
            breed=breed,
            email=email,
            password=password,
            salary=salary,
            is_admin=False
        )
    
    def verify_password(self, plain_password: str) -> bool:
        """Verify cat's password"""
        return self.password.verify(plain_password)
    
    def update_salary(self, new_salary: Salary) -> None:
        """Update cat's salary"""
        self.salary = new_salary
        self.updated_at = datetime.now(timezone.utc)
    
    def promote_to_admin(self) -> None:
        """Promote cat to admin"""
        self.is_admin = True
        self.updated_at = datetime.now(timezone.utc)
    
    def is_admin_user(self) -> bool:
        """Check if cat is admin"""
        return self.is_admin
    