import math

class Vector2D:
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y
    
    def add(self, other: 'Vector2D') -> 'Vector2D':
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def add2(self, other: 'Vector2D') -> None:
        self.x += other.x
        self.y += other.y
    
    def sub(self, other: 'Vector2D') -> 'Vector2D':
        return Vector2D(self.x - other.x, self.y - other.y)
    
    def sub2(self, other: 'Vector2D') -> None:
        self.x -= other.x
        self.y -= other.y
    
    def mult(self, scalar: float) -> 'Vector2D':
        return Vector2D(self.x * scalar, self.y * scalar)
    
    def mult2(self, scalar: float) -> None:
        self.x *= scalar
        self.y *= scalar
    
    def __str__(self) -> str:
        return f"Vector2D({self.x}, {self.y})"
    
    def length(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)
    
    def scalar_product(self, other: 'Vector2D') -> float:
        return self.x * other.x + self.y * other.y
    
    def cos(self, other: 'Vector2D') -> float:
        dot_product = self.scalar_product(other)
        len1 = self.length()
        len2 = other.length()
        
        if len1 == 0 or len2 == 0:
            return 0.0
        
        return dot_product / (len1 * len2)
    
    def equals(self, other: 'Vector2D') -> bool:
        return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)
    
    # Dunder methods (magic methods)
    def __add__(self, other: 'Vector2D') -> 'Vector2D':
        return self.add(other)
    
    def __iadd__(self, other: 'Vector2D') -> 'Vector2D':
        self.add2(other)
        return self
    
    def __sub__(self, other: 'Vector2D') -> 'Vector2D':
        return self.sub(other)
    
    def __isub__(self, other: 'Vector2D') -> 'Vector2D':
        self.sub2(other)
        return self
    
    def __mul__(self, scalar: float) -> 'Vector2D':
        return self.mult(scalar)
    
    def __imul__(self, scalar: float) -> 'Vector2D':
        self.mult2(scalar)
        return self
    
    def __rmul__(self, scalar: float) -> 'Vector2D':
        return self.mult(scalar)
    
    def __eq__(self, other: 'Vector2D') -> bool:
        return self.equals(other)
    
    def __repr__(self) -> str:
        return self.__str__()


# Demonstration
if __name__ == "__main__":
    print("=== Vector2D Demo ===")
    
    v1 = Vector2D(3, 4)
    v2 = Vector2D(1, 2)
    
    print(f"v1 = {v1}")
    print(f"v2 = {v2}")
    print(f"Length of v1: {v1.length():.2f}")
    print(f"v1 + v2 = {v1 + v2}")
    print(f"v1 - v2 = {v1 - v2}")
    print(f"v1 * 2 = {v1 * 2}")
    print(f"Dot product: {v1.scalar_product(v2)}")
    print(f"Cosine between v1 and v2: {v1.cos(v2):.4f}")
    print(f"v1 == v2? {v1 == v2}")
    
    # Test in-place operations
    v3 = Vector2D(5, 6)
    v3 += v1
    print(f"v3 after += v1: {v3}")
    v3 *= 2
    print(f"v3 after *= 2: {v3}")
