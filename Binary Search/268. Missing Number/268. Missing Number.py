class Solution(object):
    def missingNumber(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        s=set(nums)
        for i in range(1,len(s)+1):
            if i not in s:
                return i
                break            
        return 0