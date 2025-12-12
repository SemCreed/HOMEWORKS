def three_sum_sorted(arr, target):
    n = len(arr)
    for i in range(n):
        left, right = i + 1, n - 1
        while left < right:
            s = arr[i] + arr[left] + arr[right]
            if s == target:
                return (arr[i], arr[left], arr[right])
            if s < target:
                left += 1
            else:
                right -= 1
    return -1



print(three_sum_sorted([1, 2, 3, 4, 5, 6], 10))





