class Solution(object):
    def findMaxConsecutiveOnes(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        c=0
        mc=0
        for i in nums:
            if i==1:
                c+=1
                mc=max(mc,c)
            else:
                c=0
        return mc