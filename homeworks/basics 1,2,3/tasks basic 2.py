# 1. Max and min in list
def min_max(lst):
    return min(lst), max(lst)


# 2. Unique letters in string
def unique_letters(s):
    return set(s)


# 3. Reverse list without built-ins
def reverse_list(lst):
    res = []
    for i in range(len(lst) - 1, -1, -1):
        res.append(lst[i])
    return res


# 4. Reverse dictionary (string keys & values)
def reverse_dict(d):
    return {v: k for k, v in d.items()}


# 5. Custom dict.update
def dict_update(d1, d2):
    for k, v in d2.items():
        d1[k] = v
    return d1


# 6. Unique strings with length > 5
def long_unique_strings(lst):
    return {s for s in lst if len(s) > 5}


# 7. Most frequent letter
def most_frequent_letter(text):
    freq = {}
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1
    return max(freq, key=freq.get)


# 8. Group anagrams
def group_anagrams(words):
    groups = {}
    for word in words:
        key = "".join(sorted(word))
        groups.setdefault(key, []).append(word)
    return list(groups.values())


# 9. Sum 1! + 2! + ... + n! (memoization)
def factorial_sum(n, memo={}):
    if n == 0:
        return 1
    if n not in memo:
        memo[n] = n * factorial_sum(n - 1)
    return sum(memo[i] for i in range(1, n + 1))


# 10. Check vowels in columns
def check_vowel_columns(matrix):
    vowels = set("aeiouAEIOU")
    size = len(matrix)
    for col in range(size):
        count = sum(1 for row in range(size)
                    if matrix[row][col][0] in vowels)
        if count > 2:
            return False
    return True
