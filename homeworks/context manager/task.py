# file: context_managers.py

import contextlib
import functools
import json
import pickle
import logging
from typing import Any, Dict, List, Optional, Type, TypeVar, Callable
import os

T = TypeVar('T')

# =============== TASK 1: Transactional Object Saver ===============
class TransactionalObjectSaver:
    """
    Context manager for transactional object saving.
    If no error occurs, changes are kept; on error, original object is restored.
    """
    
    def __init__(self, obj: Any, save_attrs: List[str] = None):
        """
        Args:
            obj: The object to save transactionally
            save_attrs: List of attribute names to save/restore.
                       If None, saves all attributes starting with underscore.
        """
        self.obj = obj
        self.save_attrs = save_attrs
        self.original_state = {}
    
    def __enter__(self):
        """Save the original state of the object"""
        if self.save_attrs is None:
            # Save all attributes (excluding special methods)
            self.original_state = {
                attr: getattr(self.obj, attr)
                for attr in dir(self.obj)
                if not attr.startswith('__') and not attr.endswith('__')
            }
        else:
            # Save only specified attributes
            self.original_state = {
                attr: getattr(self.obj, attr)
                for attr in self.save_attrs
                if hasattr(self.obj, attr)
            }
        return self.obj
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Restore original state if an error occurred"""
        if exc_type is not None:
            # An error occurred, restore original state
            for attr, value in self.original_state.items():
                setattr(self.obj, attr, value)
            print(f"[TransactionalObjectSaver] Error occurred, restored object to original state")
            return False  # Don't suppress the exception
        # No error, keep changes
        return False


# =============== TASK 2: Error Suppressor with Logging ===============
class ErrorSuppressor:
    """
    Context manager that suppresses specified exceptions and logs them.
    """
    
    def __init__(self, *exceptions: Type[Exception], 
                 log_file: str = "error_log.txt",
                 log_level: int = logging.ERROR):
        """
        Args:
            *exceptions: Exception types to suppress
            log_file: File to log errors to
            log_level: Logging level
        """
        self.exceptions = exceptions if exceptions else (Exception,)
        self.log_file = log_file
        self.log_level = log_level
        
        # Setup logging
        self.logger = logging.getLogger('ErrorSuppressor')
        self.logger.setLevel(log_level)
        
        if not self.logger.handlers:
            handler = logging.FileHandler(log_file)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # Check if this exception should be suppressed
            if any(issubclass(exc_type, exc) for exc in self.exceptions):
                # Log the error
                self.logger.log(
                    self.log_level,
                    f"Suppressed {exc_type.__name__}: {exc_val}",
                    exc_info=(exc_type, exc_val, exc_tb)
                )
                print(f"[ErrorSuppressor] Suppressed {exc_type.__name__}: {exc_val}")
                return True  # Suppress the exception
        return False  # Don't suppress or no exception


# =============== TASK 3: Cache Manager ===============
class CacheManager:
    """
    Context manager that caches function results and saves/loads them from disk.
    """
    
    _global_cache = {}  # Shared cache across all instances
    _cache_file = "cache.pkl"
    
    def __init__(self, func: Optional[Callable] = None, cache_key: Optional[str] = None):
        """
        Args:
            func: Function to cache (optional)
            cache_key: Custom cache key (optional)
        """
        self.func = func
        self.cache_key = cache_key or (func.__name__ if func else None)
        
    def __enter__(self):
        """Load cache from disk if exists"""
        if os.path.exists(self._cache_file):
            try:
                with open(self._cache_file, 'rb') as f:
                    loaded_cache = pickle.load(f)
                    self._global_cache.update(loaded_cache)
                    print(f"[CacheManager] Loaded cache from {self._cache_file}")
            except Exception as e:
                print(f"[CacheManager] Failed to load cache: {e}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Save cache to disk"""
        try:
            with open(self._cache_file, 'wb') as f:
                pickle.dump(self._global_cache, f)
            print(f"[CacheManager] Saved cache to {self._cache_file}")
        except Exception as e:
            print(f"[CacheManager] Failed to save cache: {e}")
        return False
    
    def cached(self, *args, **kwargs):
        """Decorator to cache function results"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # Create cache key
                cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
                
                # Check cache
                if cache_key in self._global_cache:
                    print(f"[CacheManager] Cache hit for {func.__name__}")
                    return self._global_cache[cache_key]
                
                # Compute and cache
                print(f"[CacheManager] Cache miss for {func.__name__}, computing...")
                result = func(*args, **kwargs)
                self._global_cache[cache_key] = result
                return result
            return wrapper
        return decorator if self.func is None else decorator(self.func)
    
    def clear_cache(self):
        """Clear the cache"""
        self._global_cache.clear()
        print("[CacheManager] Cache cleared")
    
    def get_cache_stats(self) -> Dict:
        """Get cache statistics"""
        return {
            "size": len(self._global_cache),
            "keys": list(self._global_cache.keys())
        }


# =============== TASK 4: Mock Manager ===============
class MockManager:
    """
    Context manager to temporarily mock object attributes.
    Usage: with mock(obj, attr1=value1, attr2=value2, ...)
    """
    
    def __init__(self, obj: Any, **mock_attrs):
        """
        Args:
            obj: Object to mock
            **mock_attrs: Attributes to mock with their temporary values
        """
        self.obj = obj
        self.mock_attrs = mock_attrs
        self.original_attrs = {}
    
    def __enter__(self):
        """Save original attributes and set mock values"""
        for attr, mock_value in self.mock_attrs.items():
            if hasattr(self.obj, attr):
                self.original_attrs[attr] = getattr(self.obj, attr)
            setattr(self.obj, attr, mock_value)
            print(f"[MockManager] Mocked {attr} = {mock_value}")
        return self.obj
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Restore original attributes"""
        for attr, original_value in self.original_attrs.items():
            setattr(self.obj, attr, original_value)
            print(f"[MockManager] Restored {attr} = {original_value}")
        
        # Clean up any attributes that didn't exist before
        for attr in self.mock_attrs:
            if attr not in self.original_attrs:
                if hasattr(self.obj, attr):
                    delattr(self.obj, attr)
                    print(f"[MockManager] Removed mocked attribute {attr}")
        
        return False


# Convenience function for Task 4
def mock(obj: Any, **mock_attrs):
    """Convenience function for MockManager"""
    return MockManager(obj, **mock_attrs)


# =============== DEMONSTRATION AND TESTING ===============
class TestObject:
    """Test class for demonstrating context managers"""
    
    def __init__(self):
        self.value = 0
        self.name = "Original"
        self.data = [1, 2, 3]
    
    def risky_operation(self, divisor: int):
        """Method that might fail"""
        return 100 / divisor
    
    def expensive_computation(self, n: int) -> int:
        """Simulate expensive computation"""
        print(f"Computing factorial of {n}...")
        result = 1
        for i in range(1, n + 1):
            result *= i
        return result
    
    def get_info(self) -> str:
        return f"{self.name}: {self.value}, data={self.data}"


def demonstrate_task1():
    """Demonstrate TransactionalObjectSaver"""
    print("\n" + "="*60)
    print("TASK 1: Transactional Object Saver")
    print("="*60)
    
    obj = TestObject()
    print(f"Original object: {obj.get_info()}")
    
    # Successful transaction
    print("\n--- Successful transaction ---")
    with TransactionalObjectSaver(obj, ['value', 'name']) as safe_obj:
        safe_obj.value = 100
        safe_obj.name = "Modified"
        print(f"Modified in context: {safe_obj.get_info()}")
    
    print(f"After successful context: {obj.get_info()}")
    
    # Failed transaction
    print("\n--- Failed transaction ---")
    try:
        with TransactionalObjectSaver(obj, ['value', 'name']) as safe_obj:
            safe_obj.value = 999
            safe_obj.name = "WillFail"
            print(f"Modified before error: {safe_obj.get_info()}")
            raise ValueError("Simulated error!")
    except ValueError as e:
        print(f"Caught error: {e}")
    
    print(f"After failed context (should be restored): {obj.get_info()}")


def demonstrate_task2():
    """Demonstrate ErrorSuppressor"""
    print("\n" + "="*60)
    print("TASK 2: Error Suppressor with Logging")
    print("="*60)
    
    obj = TestObject()
    
    # Suppress specific error
    print("\n--- Suppressing ZeroDivisionError ---")
    with ErrorSuppressor(ZeroDivisionError, log_file="demo_errors.log"):
        result = obj.risky_operation(0)
        print(f"Result: {result}")  # This won't execute
    
    print("Continued execution after suppressed error")
    
    # Suppress multiple error types
    print("\n--- Suppressing multiple error types ---")
    with ErrorSuppressor(ZeroDivisionError, ValueError):
        result = obj.risky_operation(0)
    
    print("Continued after multiple error suppression")
    
    # Let through non-suppressed error
    print("\n--- Non-suppressed error (KeyError) ---")
    try:
        with ErrorSuppressor(ZeroDivisionError, ValueError):
            raise KeyError("This won't be suppressed!")
    except KeyError as e:
        print(f"Caught non-suppressed error: {e}")


def demonstrate_task3():
    """Demonstrate CacheManager"""
    print("\n" + "="*60)
    print("TASK 3: Cache Manager")
    print("="*60)
    
    obj = TestObject()
    
    # Using CacheManager as context manager
    with CacheManager() as cache_mgr:
        # Cache expensive computation
        cached_func = cache_mgr.cached(obj.expensive_computation)
        
        print("\n--- First computation (cache miss) ---")
        result1 = cached_func(5)
        print(f"Result: {result1}")
        
        print("\n--- Second computation (cache hit) ---")
        result2 = cached_func(5)
        print(f"Result: {result2}")
        
        print("\n--- Different argument (cache miss) ---")
        result3 = cached_func(10)
        print(f"Result: {result3}")
        
        print("\n--- Cache statistics ---")
        stats = cache_mgr.get_cache_stats()
        print(f"Cache size: {stats['size']}")
        print(f"Cache keys: {stats['keys']}")
    
    # New context manager should load cache
    print("\n--- New context (should load cache) ---")
    with CacheManager() as cache_mgr2:
        cached_func2 = cache_mgr2.cached(obj.expensive_computation)
        print("\n--- Should be cache hit ---")
        result = cached_func2(5)
        print(f"Result: {result}")
        
        # Clear cache
        cache_mgr2.clear_cache()
        print("\n--- After clearing cache (cache miss) ---")
        result = cached_func2(5)
        print(f"Result: {result}")


def demonstrate_task4():
    """Demonstrate MockManager"""
    print("\n" + "="*60)
    print("TASK 4: Mock Manager")
    print("="*60)
    
    obj = TestObject()
    print(f"Original object: {obj.get_info()}")
    
    # Mock attributes
    print("\n--- Mocking attributes ---")
    with mock(obj, value=999, name="MockedName", new_attr="I'm new!"):
        print(f"Inside context: {obj.get_info()}")
        print(f"New attribute: {getattr(obj, 'new_attr', 'Not found')}")
    
    print(f"\nAfter context (restored): {obj.get_info()}")
    print(f"New attribute after context: {getattr(obj, 'new_attr', 'Not found')}")
    
    # Mock with non-existent attributes
    print("\n--- Mocking non-existent attribute ---")
    with mock(obj, imaginary_value=42):
        print(f"Imaginary value inside: {getattr(obj, 'imaginary_value', 'Not found')}")
    
    print(f"Imaginary value outside: {getattr(obj, 'imaginary_value', 'Not found')}")


def demonstrate_combined_usage():
    """Demonstrate combined usage of all context managers"""
    print("\n" + "="*60)
    print("COMBINED USAGE DEMONSTRATION")
    print("="*60)
    
    class ComplexObject:
        def __init__(self):
            self.counter = 0
            self.data = []
        
        def process(self, value):
            self.counter += 1
            if value < 0:
                raise ValueError("Negative values not allowed")
            self.data.append(value)
            return value * 2
    
    obj = ComplexObject()
    
    print("Demonstrating chained context managers:")
    
    try:
        with TransactionalObjectSaver(obj) as safe_obj, \
             ErrorSuppressor(ValueError) as suppressor, \
             mock(safe_obj, counter=100) as mocked_obj:
            
            print(f"Mocked counter: {mocked_obj.counter}")
            
            # This error will be suppressed
            result = mocked_obj.process(-5)
            print(f"Result: {result}")
            
            # This will succeed
            result = mocked_obj.process(10)
            print(f"Result: {result}")
            
            print(f"Final state in context: counter={mocked_obj.counter}, data={mocked_obj.data}")
    
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    print(f"\nFinal object state: counter={obj.counter}, data={obj.data}")
    print("(Counter should be 0, data should be empty due to transactional rollback)")


def run_benchmarks():
    """Run performance benchmarks"""
    print("\n" + "="*60)
    print("PERFORMANCE BENCHMARKS")
    print("="*60)
    
    import time
    
    # Benchmark CacheManager
    print("\n--- CacheManager Benchmark ---")
    obj = TestObject()
    
    with CacheManager() as cache_mgr:
        cached_func = cache_mgr.cached(obj.expensive_computation)
        
        # First run (uncached)
        start = time.time()
        result1 = cached_func(100)
        uncached_time = time.time() - start
        
        # Second run (cached)
        start = time.time()
        result2 = cached_func(100)
        cached_time = time.time() - start
        
        print(f"Uncached: {uncached_time:.6f}s")
        print(f"Cached: {cached_time:.6f}s")
        print(f"Speedup: {uncached_time/cached_time:.2f}x")


def main():
    """Main demonstration function"""
    print("="*60)
    print("CONTEXT MANAGERS IMPLEMENTATION")
    print("="*60)
    
    # Create demo log file
    if os.path.exists("demo_errors.log"):
        os.remove("demo_errors.log")
    
    # Run all demonstrations
    demonstrate_task1()
    demonstrate_task2()
    demonstrate_task3()
    demonstrate_task4()
    demonstrate_combined_usage()
    run_benchmarks()
    
    print("\n" + "="*60)
    print("ALL TASKS COMPLETED SUCCESSFULLY!")
    print("="*60)
    
    # Show generated files
    print("\nGenerated files:")
    for file in ["demo_errors.log", "cache.pkl"]:
        if os.path.exists(file):
            print(f"  - {file} ({os.path.getsize(file)} bytes)")


if __name__ == "__main__":
    main()
