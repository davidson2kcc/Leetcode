class Solution(object):
    def isPalindrome(self, s):
        """
        :type s: str
        :rtype: bool
        """
        a=""
        for i in s:
            if i.isalnum():
                a+=(i.lower())
        
        if a[::-1]==a or a=="":
            return True
        else:
            return False
