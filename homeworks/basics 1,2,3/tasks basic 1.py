# 1. Find maximum of three numbers
def max_of_three(a, b, c):
    return max(a, b, c)


# 2. Sum of digits of a number
def sum_of_digits(n):
    return sum(int(d) for d in str(abs(n)))


# 3. Multiplication table for given digit
def multiplication_table(n):
    for i in range(1, 11):
        print(f"{n} x {i} = {n * i}")


# 4. Check valid time HH:MM:SS (24-hour format)
def is_valid_time(t):
    try:
        h, m, s = map(int, t.split(":"))
        return 0 <= h < 24 and 0 <= m < 60 and 0 <= s < 60
    except ValueError:
        return False


# 5. Check if point is inside a circle
def point_in_circle(radius, x, y):
    return x**2 + y**2 <= radius**2


# 6. Binary to decimal
def binary_to_decimal(b):
    return int(b, 2)


# 7. Decimal to binary
def decimal_to_binary(n):
    return bin(n)[2:]


# 8. Expanded form of number (70304 → 70000 + 300 + 4)
def expanded_form(n):
    digits = str(n)
    result = []
    for i, d in enumerate(digits):
        if d != '0':
            result.append(d + '0' * (len(digits) - i - 1))
    return " + ".join(result)


# 9. Levenshtein distance
def levenshtein(a, b):
    dp = [[i + j if i * j == 0 else 0 for j in range(len(b) + 1)]
          for i in range(len(a) + 1)]

    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + (a[i - 1] != b[j - 1])
            )
    return dp[-1][-1]
