class Solution(object):
    def maxProfit(self, prices):
        minimum = prices[0]
        profit = 0
        for price in prices:
            minimum = min(minimum,price)
            profit = max(profit, price - minimum)
        return profit
                
