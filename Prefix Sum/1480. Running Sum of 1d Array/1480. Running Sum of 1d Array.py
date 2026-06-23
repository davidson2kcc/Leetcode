class Solution(object):
    def runningSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        a=[]
        rs=0
        for i in range(len(nums)):
            rs+=nums[i]
            a.append(rs)
        return a
