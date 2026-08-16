# 1456. Maximum Number of Vowels in a Substring of Given Length
# Attempted
# Medium
# Topics
# premium lock icon
# Companies
# Hint
# Given a string s and an integer k, return the maximum number of vowel letters in any substring of s with length k.

# Vowel letters in English are 'a', 'e', 'i', 'o', and 'u'.



# Example 1:

# Input: s = "abciiidef", k = 3
# Output: 3
# Explanation: The substring "iii" contains 3 vowel letters.
# Example 2:

# Input: s = "aeiou", k = 2
# Output: 2
# Explanation: Any substring of length 2 contains 2 vowels.
# Example 3:

# Input: s = "leetcode", k = 3
# Output: 2
# Explanation: "lee", "eet" and "ode" contain 2 vowels.


# Constraints:

# 1 <= s.length <= 105
# s consists of lowercase English letters.
# 1 <= k <= s.length

def maxVowels(s: str, k: int) -> int:
    vowels = set('aeiou')
    max_count = 0
    current_count = 0

    # Count vowels in the first window of size k
    for i in range(k):
        if s[i] in vowels:
            current_count += 1
    max_count = current_count

    # Slide the window over the string
    for i in range(k, len(s)):
        if s[i] in vowels:
            current_count += 1
        if s[i - k] in vowels:
            current_count -= 1
        max_count = max(max_count, current_count)

    return max_count
