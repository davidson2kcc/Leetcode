class Solution(object):
    def reverseVowels(self, s):
        """
        :type s: str
        :rtype: str
        """
        b=list(s)
        
        i=0
        j=len(s)-1

        while i<j:
            while i<j and b[i] not in "aeiouAEIOU":
                i+=1
            while i<j and b[j] not in "aeiouAEIOU":
                j-=1
            b[i],b[j]=b[j],b[i]
            i+=1
            j-=1
        return "".join(b)
        