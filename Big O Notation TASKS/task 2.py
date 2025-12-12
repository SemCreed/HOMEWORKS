def two_sum_sorted(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        s = arr[left] + arr[right]
        if s == target:
            return (arr[left], arr[right])
        if s < target:
            left += 1
        else:
            right -= 1
    return -1



print(two_sum_sorted([1, 2, 3, 4, 6], 6))
