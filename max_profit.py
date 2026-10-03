# 121. Best Time to Buy and Sell Stock
# Easy
# Topics
# premium lock icon
# Companies
# You are given an array prices where prices[i] is the price of a given stock on the ith day.
#
# You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.
#
# Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.
#
#
#
# Example 1:
#
# Input: 
prices = [7,1,5,3,6,4]
# Output: 5
# Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.
# Note that buying on day 2 and selling on day 1 is not allowed because you must buy before you sell.
# Example 2:
#
# Input: prices = [7,6,4,3,1]
# Output: 0
# Explanation: In this case, no transactions are done and the max profit = 0.
#
#
# Constraints:
#
# 1 <= prices.length <= 105
# 0 <= prices[i] <= 104

def solution(prices):
    start_index = 0
    end_index = len(prices)
    new_range = []

    for i in range (start_index, end_index - 1):
        if prices[i+1] > prices[i]:
            start_index = i
            break

    # print (start_index)
    for i in range (start_index, end_index):
        new_range.append(prices[i])

    print (max(new_range))

    profit = max(new_range) - new_range[0]

    # print (profit)

    return profit


print (solution(prices))
