class Solution:
    def shortestToChar(self, s: str, c: str) -> List[int]:
        pos = []

        for i in range(len(s)):
            if s[i] == c:
                pos.append(i)

        ans = []

        for i in range(len(s)):
            mn = float('inf')

            for j in pos:
                mn = min(mn, abs(i - j))

            ans.append(mn)

        return ans
