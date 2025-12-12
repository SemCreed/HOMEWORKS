



def move_zeros(nums):
    insert_pos = 0
    for x in nums:
        if x != 0:
            nums[insert_pos] = x
            insert_pos += 1
    for i in range(insert_pos, len(nums)):
        nums[i] = 0

a = [0, 1, 0, 3, 12]
move_zeros(a)
print(a)
