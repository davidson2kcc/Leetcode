class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        l=[]
        if len(s)<len(p):
            return l 
        k=len(p)

        arr1=[0]*26
        arr2=[0]*26
        for i in range(k):
            arr2[ord(s[i])-ord("a")]+=1
            arr1[ord(p[i])-ord("a")]+=1
        

        if arr1==arr2:
            l.append(0)
        

        i=0
        for j in range(k,len(s)):
            arr2[ord(s[i])-ord("a")]-=1
            arr2[ord(s[j]) - ord("a")] += 1
            i += 1

            if arr1==arr2:
                l.append(i)
        return l