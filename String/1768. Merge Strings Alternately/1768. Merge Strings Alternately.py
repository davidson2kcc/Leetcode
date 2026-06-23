class Solution(object):
    def mergeAlternately(self, word1, word2):
        """
        :type word1: str
        :type word2: str
        :rtype: str
        """
        i = 0
        j = 0
        word3 = ""

        while i < len(word1) and j < len(word2):
            word3 += word1[i]
            word3 += word2[j]

            i += 1
            j += 1

        
        word3 += word1[i:]
        word3 += word2[j:]

        return word3