from dataclasses import dataclass

class InvalidBreedError(ValueError):
    pass

@dataclass(frozen=True)
class Breed:
    value: str
    
    def __post_init__(self):
        if not self.value or len(self.value) < 2:
            raise InvalidBreedError(f"Invalid breed: {self.value}")
    
    def __str__(self) -> str:
        return self.value