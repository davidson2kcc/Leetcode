class Solution(object):
    def thirdMax(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        s=set(nums)
        a=sorted(list(s))

        if len(a)<3:
            return max(a)
        else:
            return a[-3]

        
