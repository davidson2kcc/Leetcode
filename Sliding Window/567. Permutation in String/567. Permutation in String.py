class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:

        if len(s2)<len(s1):
            return False
        k=len(s1)

        arr1=[0]*26
        arr2=[0]*26
        for i in range(k):
            arr1[ord(s1[i])-ord("a")]+=1
            arr2[ord(s2[i])-ord("a")]+=1

        if arr1==arr2:
            return True
        i=0
        for j in range(k,len(s2)):
            arr2[ord(s2[i])-ord("a")]-=1
            arr2[ord(s2[j]) - ord("a")] += 1
            i += 1

            if arr1 == arr2:
                return True

        return False
