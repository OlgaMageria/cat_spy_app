from dataclasses import dataclass
import hashlib
import secrets

class InvalidPasswordError(ValueError):
    pass

@dataclass(frozen=True)
class Password:
    hashed_value: str
    
    @classmethod
    def create(cls, plain_password: str) -> 'Password':
        """Create a password from plain text"""
        if len(plain_password) < 8:
            raise InvalidPasswordError("Password must be at least 8 characters")
        
        salt = secrets.token_hex(32)
        hashed = hashlib.pbkdf2_hmac(
            'sha256',
            plain_password.encode(),
            salt.encode(),
            100000
        )
        return cls(f"{salt}${hashed.hex()}")
    
    def verify(self, plain_password: str) -> bool:
        """Verify if plain password matches hashed password"""
        try:
            salt, hashed = self.hashed_value.split('$')
            new_hash = hashlib.pbkdf2_hmac(
                'sha256',
                plain_password.encode(),
                salt.encode(),
                100000
            )
            return new_hash.hex() == hashed
        except ValueError:
            return False
        