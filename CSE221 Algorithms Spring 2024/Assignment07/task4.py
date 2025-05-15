inp = open('input4.txt', 'r')
outp = open('output4.txt', 'w')

n, t = tuple(map(int, inp.readline().split()))
coins = list(map(int, inp.readline().split()))

dp = [float('inf')]*(t+1)
dp[0] = 0

def min_coin(n, t):
   
   for i in range(1, t+1):
      for j in coins:
       if i-j >= 0:
         if dp[i] > 1+dp[i-j]:
           dp[i] = 1+dp[i-j]

   if dp[t] != float('inf'):
     return dp[t]
   return -1

outp.write(str(min_coin(n, t)))