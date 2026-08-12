# 1732. Find the Highest Altitude
# Easy
# Topics
# premium lock icon
# Companies
# Hint
# There is a biker going on a road trip. The road trip consists of n + 1 points at various altitudes. The biker starts his trip on point 0 with altitude equal 0.
#
# You are given an integer array gain of length n where gain[i] is the net gain in altitude between points i​​​​​​ and i + 1 for all (0 <= i < n). Return the highest altitude of a point.
#
#
#
# Example 1:
#
# Input: gain = [-5,1,5,0,-7]
# Output: 1
# Explanation: The altitudes are [0,-5,-4,1,1,-6]. The highest is 1.
# Example 2:
#
# Input: gain = [-4,-3,-2,-1,4,3,2]
# Output: 0
# Explanation: The altitudes are [0,-4,-7,-9,-10,-6,-3,-1]. The highest is 0.
#
#
# Constraints:
#
# n == gain.length
# 1 <= n <= 100
# -100 <= gain[i] <= 100
gain = [-5,1,5,0,-7]

def solution(gain):
    coordinates_gain = []

    for i in range(len(gain)-1):
        coordinates_gain.append((gain[i+1]-gain[i],i))
    print (coordinates_gain)

    for pair in coordinates_gain:
        if max(pair[0] for pair in coordinates_gain):
            return pair[1] + 1

print (solution(gain))
