from collections import Counter
class Solution(object):
    def majorityElement(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        candidate = 0
        count = 0

        for i in nums:
            if count == 0:
                candidate = i

            if i == candidate:
                count += 1
            else:
                count -= 1

        return candidate