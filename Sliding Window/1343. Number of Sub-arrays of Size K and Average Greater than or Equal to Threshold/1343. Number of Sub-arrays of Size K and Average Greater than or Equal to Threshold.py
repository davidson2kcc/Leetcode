class Solution:
    def numOfSubarrays(self, arr: List[int], k: int, threshold: int) -> int:
        
        if k>len(arr):
            return 0
        
        s=sum(arr[:k])
        c=0
        if s//k >=threshold:
            c=1
        
        for i in range(k,len(arr)):
            s-=arr[i-k]
            s+=arr[i]

            if s//k >=threshold:
                c+=1
        return c
