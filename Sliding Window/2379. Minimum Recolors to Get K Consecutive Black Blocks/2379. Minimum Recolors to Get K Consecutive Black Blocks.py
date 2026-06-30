class Solution:
    def minimumRecolors(self, blocks: str, k: int) -> int:
        c=0
        m=0
        for i in range(k):
            if c<=k :
                if blocks[i]=="W":
                    c+=1
        m=c
        if k==len(blocks):
            return m
            exit()

        
        for j in range(k,len(blocks)):
            if blocks[j]=="W":
                c+=1
            if blocks[j-k]=="W":
                c-=1
            m=min(m,c)
        return m
                
                