class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:
        zero=0
        m=0
        l=0
        r=0

        for r in range(len(nums)):
            if nums[r]==0:
                zero+=1
            if zero<=k:
                m=max(m,r-l+1)
            while(zero>k):
                if nums[l]==0:
                    zero-=1
                l+=1
        m=max(m,r-l+1)
        return m
                