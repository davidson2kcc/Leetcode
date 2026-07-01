class Solution:
    def firstUniqChar(self, s: str) -> int:
        f=0
        for i in range(len(s)):
            if s[i] not in s[i+1:] and s[i] not in s[:i]:
                f=1
                return i
      
                
        if not f:
            return -1
