class Solution:
    def validUtf8(self, data: List[int]) -> bool:

        count = 0

        for x in data:

            if count == 0:

                if x < 128:
                    count = 0

                elif x >= 128 and x < 192:
                    return False

                elif x < 224:
                    count = 1

                elif x < 240:
                    count = 2

                elif x < 248:
                    count = 3

                else:
                    return False

            else:

                if x >= 128 and x < 192:
                    count -= 1
                else:
                    return False

        return count == 0