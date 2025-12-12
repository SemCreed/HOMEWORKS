# 1) Check if string is a palindrome
def is_palindrome(s: str) -> bool:
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True

print(is_palindrome("hello"))
print(is_palindrome("python"))
print(is_palindrome("pop"))
