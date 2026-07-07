class Solution:
    def uniquePathsIII(self, grid: List[List[int]]) -> int:
        way=0
        def findpath(i,j,sol,path):

            nonlocal way
        
            if i<0 or i>=m or j<0 or j>=n or grid[i][j]==-1 or sol[i][j]==1:
                return 

            if i==c and j==d and sol[i][j]==0 and grid [i][j]==2:
                sol[i][j]=1

                if z==path:
                    way+=1
                    
                sol[i][j]=0

                return

            sol[i][j]= 1

            findpath(i+1,j,sol,path+1)

            findpath(i,j+1,sol,path+1)

            findpath(i-1,j,sol,path+1)

            findpath(i,j-1,sol,path+1)
            
            sol[i][j]=0

            return 

        m=len(grid)
        n=len(grid[0])
        sol=[[0]*n for _ in range(m)]
        z=2
        for i in range(m):
            for j in range(n):
                if grid[i][j]==1:
                    a,b=i,j
                if grid[i][j]==2:
                    c,d=i,j
                if grid[i][j]==0:
                    z+=1
        
        findpath(a,b,sol,1)
        return way

 
