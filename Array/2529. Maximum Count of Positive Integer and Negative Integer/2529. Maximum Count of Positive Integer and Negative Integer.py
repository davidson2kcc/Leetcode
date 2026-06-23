class Solution(object):
    def maximumCount(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        c1=0
        c2=0
        for i in nums:
            if i ==0:
                continue
            elif i>0:
                c1+=1
            else:
                c2+=1
        if c1>c2:
            return c1
        else:
            return c2
