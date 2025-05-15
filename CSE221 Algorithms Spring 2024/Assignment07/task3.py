inp = open('input3.txt', 'r')
outp = open('output3.txt', 'w')

n = int(inp.readline())

dp = [0]*(n+1)
dp[0], dp[1] = 1, 1

def staircount(n):

   if n <= 1:
      return 1
   
   for i in range (2, n+1):
      dp[i] = dp[i-1] + dp[i-2]
      
   return dp[n]

outp.write(str(staircount(n)))