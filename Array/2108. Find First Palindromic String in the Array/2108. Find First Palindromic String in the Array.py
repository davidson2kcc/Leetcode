class Solution(object):
    def firstPalindrome(self, words):
        """
        :type words: List[str]
        :rtype: str
        """
        s=""
        for i in words:
            if i==i[::-1]:
                s+=i
                return s
                break
        else:
            return s