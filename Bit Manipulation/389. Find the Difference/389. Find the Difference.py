class Solution(object):
    def findTheDifference(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: str
        """
        d = {}

        for ch in s:
            d[ch] = d.get(ch, 0) + 1

        for ch in t:
            if ch not in d or d[ch] == 0:
                return ch

            d[ch] -= 1