class Solution(object):
    def removeDuplicates(self, nums):
        temp=list(set(nums))
        temp.sort()
        for i in range(len(temp)):
            nums[i]=temp[i]
        print(nums)
        return len(temp)