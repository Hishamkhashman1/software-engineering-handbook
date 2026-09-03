# given two integer arrays nums1 and nums2
# Merge nums1 and nums2 into a single array sorted in non-decreasing order
# 
# Merge nums1 and nums2 into a single array sorted in non-decreasing order.
#
# The final sorted array should not be returned by the function, but instead be stored inside the array nums1. 
# To accommodate this, nums1 has a length of m + n, where the first m elements denote the elements that should be merged, 
# and the last n elements are set to 0 and should be ignored. nums2 has a length of n.



# Example 1 
#
nums1 =  [1,2,3,0,0,0]
m = 3
nums2 = [2,5,6]
n = 3
# output [1,2,2,3,5,6]

def solution(nums1, nums2, m, n):
    merged = []

    for i in range (0,m):
        merged.append(nums1[i])

    for i in range (0,n):
        merged.append(nums2[i])

    merged.sort()
    nums1[:] = merged

    return nums1


print (solution(nums1,nums2,m,n))


