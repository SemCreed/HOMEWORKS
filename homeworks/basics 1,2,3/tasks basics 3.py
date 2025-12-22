# 1. Lambda: divisible by 5
div_by_5 = lambda x: x % 5 == 0


# 2. Print numbers from n to 1 (recursion)
def print_n_to_1(n):
    if n == 0:
        return
    print(n)
    print_n_to_1(n - 1)


# 3. Power function (recursion)
def power(base, exp):
    if exp == 0:
        return 1
    return base * power(base, exp - 1)


# 4. Fibonacci sequence
def fibonacci(n):
    if n <= 0:
        return []
    seq = [1, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq[:n]


# 5. Flatten nested list (recursion)
def flatten(lst):
    res = []
    for item in lst:
        if isinstance(item, list):
            res.extend(flatten(item))
        else:
            res.append(item)
    return res


# 6. Palindrome check (recursion)
def is_palindrome(s):
    if len(s) <= 1:
        return True
    return s[0] == s[-1] and is_palindrome(s[1:-1])


# 7. Safe index access with exceptions
def get_element(lst, index):
    try:
        return lst[index]
    except IndexError:
        return None


# 8. Retry decorator
def retry(func):
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except Exception:
                continue
    return wrapper


# 9. Lambda: sum of digits
sum_digits = lambda n: sum(int(d) for d in str(abs(n)))
