class Solution(object):
    def sortedSquares(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        nums1=[]
        for i in nums:
            nums1.append(i**2)
        nums1.sort()
        return nums1
