class Solution(object):
    def maximumWealth(self, accounts):
        """
        :type accounts: List[List[int]]
        :rtype: int
        """
        Sum=[]
        for i in accounts:
            Sum.append(sum(i))
        return max(Sum)
        