class Solution(object):
    def merge(self, nums1, m, nums2, n):
        """
        :type nums1: List[int]
        :type m: int
        :type nums2: List[int]
        :type n: int
        :rtype: None Do not return anything, modify nums1 in-place instead.
        """
        i=0
        j=0

        while(i<len(nums1) and j<len(nums2)):
            if nums1[i]==0:
                nums1[i]=nums2[j]
                i+=1
                j+=1
            else:
                i+=1
        print(nums1.sort())