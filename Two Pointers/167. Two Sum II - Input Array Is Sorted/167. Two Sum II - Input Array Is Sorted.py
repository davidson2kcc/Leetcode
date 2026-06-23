class Solution(object):
    def twoSum(self, numbers, target):
        """
        :type numbers: List[int]
        :type target: int
        :rtype: List[int]
        """
        i=0
        j=len(numbers)-1

        while(i<j):
            curr=numbers[i]+numbers[j]
            if curr ==target :
                return [i+1,j+1]
            
            elif curr<target:
                i+=1
            else:
                j-=1
            