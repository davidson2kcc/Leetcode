class Solution:
    def findMinArrowShots(self, points: List[List[int]]) -> int:
        points.sort(key=lambda x: x[1])
        count=1
        a=points[0][1]
        for i in range(1,len(points)):
            if a < points[i][0]:
                count+=1
                a=points[i][1]
        return count