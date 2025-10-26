from dataclasses import dataclass
from decimal import Decimal

class InvalidSalaryError(ValueError):
    pass

@dataclass(frozen=True)
class Salary:
    amount: Decimal
    
    def __post_init__(self):
        if self.amount < 0:
            raise InvalidSalaryError(f"Salary cannot be negative: {self.amount}")
    
    def increase(self, percentage: float) -> 'Salary':
        new_amount = self.amount * (1 + Decimal(str(percentage)))
        return Salary(new_amount)
    
    def __str__(self) -> str:
        return f"${self.amount}"