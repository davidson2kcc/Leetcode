class Solution:
    def maxVowels(self, s: str, k: int) -> int:
        if len(s)<k:
            return 0
        

        c=0
        for i in range(k):
            if s[i] in "aeiouAEIOU":
                c+=1

        if k==len(s):
            return c
        m=c
        for j in range(k,len(s)):
            if s[j-k] in "aeiouAEIOU":
                c-=1
            if s[j] in "aeiouAEIOU":
                c+=1
            
            m=max(m,c)
        return m
