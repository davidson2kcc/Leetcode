class Solution(object):
    def findMedianSortedArrays(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: float
        """
        c=sorted(nums1+nums2)
        n=len(c)
        d=c[n//2]
        e=c[(n//2)-1]
        if n%2==1:
            return float(d)
        else:
            return (d+e)/2.0
        
              
                 