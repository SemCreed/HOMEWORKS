



def single_number(nums):
    res = 0
    for x in nums:
        res ^= x
    return res



print(single_number([4, 1, 2, 1, 2]))
