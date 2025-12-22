from typing import Iterable, Any, List, Tuple, Generator
import itertools
import math

# =============== TASK 1: Chain Sequences Iterator ===============
class ChainSequences:
    """Iterator to chain multiple sequences together"""
    
    def __init__(self, *sequences):
        self.sequences = sequences
        self.current_sequence_index = 0
        self.current_iterator = iter(self.sequences[0]) if self.sequences else iter([])
    
    def __iter__(self):
        return self
    
    def __next__(self):
        while True:
            try:
                return next(self.current_iterator)
            except StopIteration:
                # Move to next sequence
                self.current_sequence_index += 1
                if self.current_sequence_index >= len(self.sequences):
                    raise StopIteration
                self.current_iterator = iter(self.sequences[self.current_sequence_index])


def chain_sequences(*sequences):
    """Generator function version of chain sequences"""
    for seq in sequences:
        yield from seq


# =============== TASK 2: Zip Sequences Iterator ===============
class ZipSequences:
    """Iterator to zip multiple sequences together"""
    
    def __init__(self, *sequences):
        self.sequences = sequences
        self.iterators = [iter(seq) for seq in sequences]
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            result = []
            for it in self.iterators:
                result.append(next(it))
            return tuple(result)
        except StopIteration:
            raise StopIteration


def zip_sequences(*sequences):
    """Generator function version of zip sequences"""
    iterators = [iter(seq) for seq in sequences]
    while True:
        try:
            result = []
            for it in iterators:
                result.append(next(it))
            yield tuple(result)
        except StopIteration:
            return


# =============== TASK 3: Prime Number Generator ===============
def generate_primes(n: int) -> Generator[int, None, None]:
    """Generate all prime numbers less than n"""
    if n <= 1:
        return
    
    # Special case: 1 is sometimes considered prime, sometimes not
    # We'll include it as requested in the example
    yield 1
    
    # Generate primes using Sieve of Eratosthenes
    if n <= 2:
        return
    
    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False
    
    for i in range(2, int(math.sqrt(n)) + 1):
        if is_prime[i]:
            for j in range(i*i, n, i):
                is_prime[j] = False
    
    for i in range(2, n):
        if is_prime[i]:
            yield i


# =============== TASK 4: Combinations Generator ===============
def generate_combinations(sequence: List[Any], k: int) -> Generator[Tuple, None, None]:
    """Generate all combinations of length k from sequence"""
    n = len(sequence)
    
    if k > n or k <= 0:
        return
    
    # Generate combinations using recursion
    def _combine(start: int, current: List[Any]):
        if len(current) == k:
            yield tuple(current)
            return
        
        for i in range(start, n):
            current.append(sequence[i])
            yield from _combine(i + 1, current)
            current.pop()
    
    yield from _combine(0, [])


# =============== TASK 5: Multi-dimensional Array Iterator ===============
class FlattenIterator:
    """Iterator to flatten nested lists without creating additional lists"""
    
    def __init__(self, nested_list):
        self.stack = [(nested_list, 0)]  # (list, current_index)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        while self.stack:
            current_list, index = self.stack[-1]
            
            if index >= len(current_list):
                self.stack.pop()
                continue
            
            # Update index for next call
            self.stack[-1] = (current_list, index + 1)
            
            element = current_list[index]
            
            if isinstance(element, list):
                # Push nested list onto stack
                self.stack.append((element, 0))
            else:
                return element
        
        raise StopIteration


def flatten_iterator_generator(nested_list):
    """Generator function version of flatten iterator"""
    for element in nested_list:
        if isinstance(element, list):
            yield from flatten_iterator_generator(element)
        else:
            yield element


# =============== DEMONSTRATION FUNCTIONS ===============
def demonstrate_all_tasks():
    print("=" * 60)
    print("ITERATOR AND GENERATOR TASKS DEMONSTRATION")
    print("=" * 60)
    
    # Task 1: Chain Sequences
    print("\n1. CHAIN SEQUENCES ITERATOR")
    print("-" * 40)
    
    # Using class
    print("Using ChainSequences class:")
    chain_class = ChainSequences([1, 2, 3], [4], [5])
    result1_class = []
    for item in chain_class:
        result1_class.append(item)
    print(f"  ChainSequences([1, 2, 3], [4], [5]) = {result1_class}")
    
    # Using generator function
    print("\nUsing chain_sequences generator function:")
    result1_gen = list(chain_sequences([1, 2, 3], [4], [5]))
    print(f"  chain_sequences([1, 2, 3], [4], [5]) = {result1_gen}")
    
    # More complex example
    print("\nComplex example with strings:")
    result1_complex = list(chain_sequences(
        "Hello", 
        ["World", "!"], 
        (42, 3.14)
    ))
    print(f"  chain_sequences('Hello', ['World', '!'], (42, 3.14)) = {result1_complex}")
    
    # Task 2: Zip Sequences
    print("\n\n2. ZIP SEQUENCES ITERATOR")
    print("-" * 40)
    
    # Using class
    print("Using ZipSequences class:")
    zip_class = ZipSequences([1, 2], [3, 4], [5, 6])
    result2_class = []
    for item in zip_class:
        result2_class.append(item)
    print(f"  ZipSequences([1, 2], [3, 4], [5, 6]) = {result2_class}")
    
    # Using generator function
    print("\nUsing zip_sequences generator function:")
    result2_gen = list(zip_sequences([1, 2], [3, 4], [5, 6]))
    print(f"  zip_sequences([1, 2], [3, 4], [5, 6]) = {result2_gen}")
    
    # Different length sequences
    print("\nDifferent length sequences (should stop at shortest):")
    result2_diff = list(zip_sequences([1, 2, 3], [4, 5], [6]))
    print(f"  zip_sequences([1, 2, 3], [4, 5], [6]) = {result2_diff}")
    
    # Task 3: Prime Number Generator
    print("\n\n3. PRIME NUMBER GENERATOR")
    print("-" * 40)
    
    # Test case from requirements
    print("Prime numbers less than 8:")
    primes_8 = list(generate_primes(8))
    print(f"  generate_primes(8) = {primes_8}")
    
    # More test cases
    test_cases = [1, 2, 10, 20, 50]
    for n in test_cases:
        primes = list(generate_primes(n))
        print(f"  generate_primes({n:2d}) = {primes}")
    
    # Demonstrate generator behavior (not storing all in memory)
    print("\nGenerating first 10 prime numbers using generator (one at a time):")
    prime_gen = generate_primes(100)
    first_10_primes = []
    for i, prime in enumerate(prime_gen):
        if i >= 10:
            break
        first_10_primes.append(prime)
    print(f"  First 10 primes from generate_primes(100): {first_10_primes}")
    
    # Task 4: Combinations Generator
    print("\n\n4. COMBINATIONS GENERATOR")
    print("-" * 40)
    
    # Test case from requirements
    print("Combinations of length 2 from [1, 2, 3]:")
    combos = list(generate_combinations([1, 2, 3], 2))
    print(f"  generate_combinations([1, 2, 3], 2) = {combos}")
    
    # More test cases
    test_cases = [
        ([1, 2, 3, 4], 2),
        (['A', 'B', 'C', 'D'], 3),
        ([1, 2, 3], 1),
        ([1, 2, 3], 3),
    ]
    
    for seq, k in test_cases:
        combos = list(generate_combinations(seq, k))
        print(f"\n  generate_combinations({seq}, {k}) = {combos}")
    
    # Edge cases
    print("\nEdge cases:")
    print(f"  generate_combinations([], 2) = {list(generate_combinations([], 2))}")
    print(f"  generate_combinations([1, 2], 3) = {list(generate_combinations([1, 2], 3))}")
    print(f"  generate_combinations([1, 2, 3], 0) = {list(generate_combinations([1, 2, 3], 0))}")
    
    # Task 5: Multi-dimensional Array Iterator
    print("\n\n5. MULTI-DIMENSIONAL ARRAY ITERATOR")
    print("-" * 40)
    
    # Test case from requirements
    print("Flattening [1, 2, [3, [4], 5]]:")
    
    # Using class
    print("\nUsing FlattenIterator class:")
    flatten_class = FlattenIterator([1, 2, [3, [4], 5]])
    result5_class = []
    for item in flatten_class:
        result5_class.append(item)
    print(f"  FlattenIterator([1, 2, [3, [4], 5]]) = {result5_class}")
    
    # Using generator function
    print("\nUsing flatten_iterator_generator:")
    result5_gen = list(flatten_iterator_generator([1, 2, [3, [4], 5]]))
    print(f"  flatten_iterator_generator([1, 2, [3, [4], 5]]) = {result5_gen}")
    
    # More complex test cases
    test_cases = [
        [1, [2, [3, [4, [5]]]]],
        [[1, 2], [3, 4], [5, 6]],
        [1, [2, 3], [[4, 5], [6, [7, 8]]]],
        [],
        [[[]]],
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        result = list(flatten_iterator_generator(test_case))
        print(f"\n  Test {i}: {test_case}")
        print(f"    Result: {result}")
    
    # Demonstrate memory efficiency
    print("\n\nMemory Efficiency Demonstration:")
    print("-" * 40)
    
    # Create a large nested structure
    large_nested = []
    current = large_nested
    for i in range(1000):
        current.append(i)
        new_list = []
        current.append(new_list)
        current = new_list
    
    print("Created a deeply nested list with 1000 levels")
    print("Using generator to flatten (memory efficient):")
    
    # Count elements without storing them all
    count = 0
    for _ in flatten_iterator_generator(large_nested):
        count += 1
        if count % 100 == 0:
            print(f"  Processed {count} elements...")
    
    print(f"Total elements: {count}")


# =============== ADDITIONAL UTILITY FUNCTIONS ===============
def demonstrate_alternatives():
    """Show alternative implementations using itertools"""
    print("\n" + "=" * 60)
    print("ALTERNATIVE IMPLEMENTATIONS USING BUILT-IN ITERTOOLS")
    print("=" * 60)
    
    # Task 1 alternative
    print("\n1. chain_sequences using itertools.chain:")
    result = list(itertools.chain([1, 2, 3], [4], [5]))
    print(f"  itertools.chain([1, 2, 3], [4], [5]) = {result}")
    
    # Task 2 alternative
    print("\n2. zip_sequences using built-in zip:")
    result = list(zip([1, 2], [3, 4], [5, 6]))
    print(f"  zip([1, 2], [3, 4], [5, 6]) = {result}")
    
    # Task 4 alternative
    print("\n4. generate_combinations using itertools.combinations:")
    result = list(itertools.combinations([1, 2, 3], 2))
    print(f"  itertools.combinations([1, 2, 3], 2) = {result}")
    
    # Task 5 alternative (though it creates intermediate lists)
    print("\n5. Flattening using recursion (creates new lists):")
    
    def flatten_recursive(lst):
        result = []
        for item in lst:
            if isinstance(item, list):
                result.extend(flatten_recursive(item))
            else:
                result.append(item)
        return result
    
    result = flatten_recursive([1, 2, [3, [4], 5]])
    print(f"  flatten_recursive([1, 2, [3, [4], 5]]) = {result}")


# =============== PERFORMANCE COMPARISON ===============
def performance_comparison():
    """Compare performance of different implementations"""
    import time
    
    print("\n" + "=" * 60)
    print("PERFORMANCE COMPARISON")
    print("=" * 60)
    
    # Test data
    large_list = list(range(10000))
    nested_list = [[i, [i+1, [i+2]]] for i in range(1000)]
    
    # Task 1: Chain
    print("\n1. Chain performance:")
    
    start = time.time()
    list(chain_sequences(large_list, large_list, large_list))
    custom_time = time.time() - start
    
    start = time.time()
    list(itertools.chain(large_list, large_list, large_list))
    itertools_time = time.time() - start
    
    print(f"  Custom implementation: {custom_time:.6f}s")
    print(f"  itertools.chain: {itertools_time:.6f}s")
    print(f"  Ratio: {custom_time/itertools_time:.2f}x")
    
    # Task 3: Primes
    print("\n3. Prime generation performance:")
    
    n = 10000
    start = time.time()
    list(generate_primes(n))
    custom_time = time.time() - start
    
    print(f"  generate_primes({n}): {custom_time:.6f}s")
    print(f"  Generated {len(list(generate_primes(n)))} primes")
    
    # Task 5: Flatten
    print("\n5. Flatten performance:")
    
    start = time.time()
    list(flatten_iterator_generator(nested_list))
    generator_time = time.time() - start
    
    print(f"  Generator implementation: {generator_time:.6f}s")
    print(f"  Processed {len(list(flatten_iterator_generator(nested_list)))} elements")


if __name__ == "__main__":
    demonstrate_all_tasks()
    demonstrate_alternatives()
    performance_comparison()
    
    print("\n" + "=" * 60)
    print("ALL TASKS COMPLETED SUCCESSFULLY!")
    print("=" * 60)
