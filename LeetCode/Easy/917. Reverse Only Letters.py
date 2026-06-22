class Solution(object):
    def reverseOnlyLetters(self, s):
        """
        :type s: str
        :rtype: str
        """
        b=list(s)
        i=0
        j=len(s)-1
        while i<j:
            while i<j and not b[i].isalpha():
                i+=1
            while i<j and not b[j].isalpha():
                j-=1

            b[i],b[j]=b[j],b[i]
            i+=1
            j-=1
        return ("".join(b))