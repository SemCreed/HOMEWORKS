import math

class RationalFraction:
    def __init__(self, numerator: int, denominator: int = 1):
        if denominator == 0:
            raise ValueError("Denominator cannot be zero")
        
        self.numerator = numerator
        self.denominator = denominator
        self._reduce()
    
    def _reduce(self) -> None:
        """Reduce the fraction to its simplest form"""
        gcd_val = math.gcd(abs(self.numerator), abs(self.denominator))
        self.numerator //= gcd_val
        self.denominator //= gcd_val
        
        # Ensure denominator is positive
        if self.denominator < 0:
            self.numerator = -self.numerator
            self.denominator = -self.denominator
    
    def __add__(self, other: 'RationalFraction') -> 'RationalFraction':
        """Addition of fractions (returns new reduced fraction)"""
        if not isinstance(other, RationalFraction):
            other = RationalFraction(other, 1)
        
        new_numerator = self.numerator * other.denominator + other.numerator * self.denominator
        new_denominator = self.denominator * other.denominator
        return RationalFraction(new_numerator, new_denominator)
    
    def __iadd__(self, other: 'RationalFraction') -> 'RationalFraction':
        """Adding other fraction to current in-place"""
        if not isinstance(other, RationalFraction):
            other = RationalFraction(other, 1)
        
        self.numerator = self.numerator * other.denominator + other.numerator * self.denominator
        self.denominator = self.denominator * other.denominator
        self._reduce()
        return self
    
    def __sub__(self, other: 'RationalFraction') -> 'RationalFraction':
        """Subtraction of fractions (returns new reduced fraction)"""
        if not isinstance(other, RationalFraction):
            other = RationalFraction(other, 1)
        
        new_numerator = self.numerator * other.denominator - other.numerator * self.denominator
        new_denominator = self.denominator * other.denominator
        return RationalFraction(new_numerator, new_denominator)
    
    def __isub__(self, other: 'RationalFraction') -> 'RationalFraction':
        """Subtracting other fraction from current in-place"""
        if not isinstance(other, RationalFraction):
            other = RationalFraction(other, 1)
        
        self.numerator = self.numerator * other.denominator - other.numerator * self.denominator
        self.denominator = self.denominator * other.denominator
        self._reduce()
        return self
    
    def __mul__(self, other: 'RationalFraction') -> 'RationalFraction':
        """Multiplication of fractions (returns new reduced fraction)"""
        if not isinstance(other, RationalFraction):
            other = RationalFraction(other, 1)
        
        new_numerator = self.numerator * other.numerator
        new_denominator = self.denominator * other.denominator
        return RationalFraction(new_numerator, new_denominator)
    
    def __imul__(self, other: 'RationalFraction') -> 'RationalFraction':
        """Multiplying current fraction by another in-place"""
        if not isinstance(other, RationalFraction):
            other = RationalFraction(other, 1)
        
        self.numerator *= other.numerator
        self.denominator *= other.denominator
        self._reduce()
        return self
    
    def __truediv__(self, other: 'RationalFraction') -> 'RationalFraction':
        """Division of fractions (returns new reduced fraction)"""
        if not isinstance(other, RationalFraction):
            other = RationalFraction(other, 1)
        
        if other.numerator == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        
        new_numerator = self.numerator * other.denominator
        new_denominator = self.denominator * other.numerator
        return RationalFraction(new_numerator, new_denominator)
    
    def __itruediv__(self, other: 'RationalFraction') -> 'RationalFraction':
        """Dividing current fraction by another in-place"""
        if not isinstance(other, RationalFraction):
            other = RationalFraction(other, 1)
        
        if other.numerator == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        
        self.numerator *= other.denominator
        self.denominator *= other.numerator
        self._reduce()
        return self
    
    def to_float(self) -> float:
        """Returns float representation of fraction"""
        return self.numerator / self.denominator
    
    def __eq__(self, other: object) -> bool:
        """Comparing two fractions for equality"""
        if not isinstance(other, RationalFraction):
            if isinstance(other, (int, float)):
                return abs(self.to_float() - other) < 1e-10
            return False
        
        # Fractions are equal if cross products are equal
        return self.numerator * other.denominator == other.numerator * self.denominator
    
    def __str__(self) -> str:
        return f"{self.numerator}/{self.denominator}"
    
    def __repr__(self) -> str:
        return f"RationalFraction({self.numerator}, {self.denominator})"


# Examples for every method
def demonstrate_rational_fraction():
    print("=== RationalFraction Class Demonstration ===\n")
    
    # 1. Initialization and __str__/__repr__
    print("1. Initialization:")
    rf1 = RationalFraction(4, 8)  # Will be reduced to 1/2
    rf2 = RationalFraction(3, 4)
    rf3 = RationalFraction(6, 12)  # Will be reduced to 1/2
    print(f"rf1 = {rf1}")  # 1/2
    print(f"rf2 = {rf2}")  # 3/4
    print(f"rf3 = {rf3}")  # 1/2
    print(f"repr(rf1) = {repr(rf1)}")
    
    # 2. __eq__ method
    print("\n2. Equality comparison:")
    print(f"rf1 == rf3? {rf1 == rf3}")  # True
    print(f"rf1 == rf2? {rf1 == rf2}")  # False
    print(f"rf1 == 0.5? {rf1 == 0.5}")  # True
    print(f"rf2 == 0.75? {rf2 == 0.75}")  # True
    
    # 3. to_float() method
    print("\n3. Float conversion:")
    print(f"rf1.to_float() = {rf1.to_float()}")  # 0.5
    print(f"rf2.to_float() = {rf2.to_float()}")  # 0.75
    
    # 4. __add__ and __iadd__ methods
    print("\n4. Addition operations:")
    # Regular addition (returns new object)
    result_add = rf1 + rf2
    print(f"rf1 + rf2 = {result_add}")  # 1/2 + 3/4 = 5/4
    
    # In-place addition
    rf_temp = RationalFraction(1, 3)
    rf_temp += RationalFraction(2, 3)
    print(f"1/3 += 2/3 = {rf_temp}")  # 1/1
    
    # 5. __sub__ and __isub__ methods
    print("\n5. Subtraction operations:")
    # Regular subtraction
    result_sub = rf2 - rf1
    print(f"rf2 - rf1 = {result_sub}")  # 3/4 - 1/2 = 1/4
    
    # In-place subtraction
    rf_temp = RationalFraction(5, 6)
    rf_temp -= RationalFraction(1, 6)
    print(f"5/6 -= 1/6 = {rf_temp}")  # 2/3
    
    # 6. __mul__ and __imul__ methods
    print("\n6. Multiplication operations:")
    # Regular multiplication
    result_mul = rf1 * rf2
    print(f"rf1 * rf2 = {result_mul}")  # 1/2 * 3/4 = 3/8
    
    # In-place multiplication
    rf_temp = RationalFraction(2, 3)
    rf_temp *= RationalFraction(3, 4)
    print(f"2/3 *= 3/4 = {rf_temp}")  # 1/2
    
    # 7. __truediv__ and __itruediv__ methods
    print("\n7. Division operations:")
    # Regular division
    result_div = rf2 / rf1
    print(f"rf2 / rf1 = {result_div}")  # (3/4) / (1/2) = 3/2
    
    # In-place division
    rf_temp = RationalFraction(4, 5)
    rf_temp /= RationalFraction(2, 5)
    print(f"4/5 /= 2/5 = {rf_temp}")  # 2/1
    
    # 8. Automatic reduction demonstration
    print("\n8. Automatic reduction:")
    rf_complex = RationalFraction(8, 12)
    print(f"8/12 automatically reduced to: {rf_complex}")  # 2/3
    
    # 9. Operations with integers
    print("\n9. Operations with integers:")
    rf_int_op = RationalFraction(1, 2)
    print(f"1/2 + 1 = {rf_int_op + 1}")  # 3/2
    print(f"1/2 * 3 = {rf_int_op * 3}")  # 3/2
    
    # 10. Chain of operations
    print("\n10. Chain of operations:")
    result_chain = (RationalFraction(1, 2) + RationalFraction(1, 3)) * RationalFraction(2, 5)
    print(f"(1/2 + 1/3) * 2/5 = {result_chain}")  # (5/6) * (2/5) = 1/3
    
    # 11. Edge cases
    print("\n11. Edge cases:")
    try:
        rf_zero_denom = RationalFraction(1, 0)
    except ValueError as e:
        print(f"Error creating fraction with zero denominator: {e}")
    
    try:
        rf_divide_zero = RationalFraction(1, 2) / RationalFraction(0, 1)
    except ZeroDivisionError as e:
        print(f"Error dividing by zero: {e}")
    
    # 12. Negative fractions
    print("\n12. Negative fractions:")
    rf_neg = RationalFraction(-3, 4)
    print(f"-3/4 = {rf_neg}")
    rf_neg2 = RationalFraction(3, -4)
    print(f"3/(-4) automatically normalized to: {rf_neg2}")  # -3/4
    print(f"-3/4 + 1/2 = {rf_neg + RationalFraction(1, 2)}")  # -1/4


if __name__ == "__main__":
    demonstrate_rational_fraction()
