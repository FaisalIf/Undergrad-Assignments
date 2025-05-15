inp = open("input4.txt", "r")
outp = open("output4.txt", "w")

v, e = tuple(map(int, inp.readline().split(" ")))
di = {}

for i in range(v+1):
   di[i] = []
for i in range(e):
   a, b = tuple(map(int, inp.readline().split(" ")))
   di[a].append((b))

colour = ["white"]*(v+1)

def dfs(g, s):
   
   result = True
   colour[s] = "gray"

   for v in g[s]:
      if colour[v] == "gray":
         result = False

      if colour[v] == "white":
         colour[v] = "gray"
         result = result and dfs(g, v)
   colour[s] = "black"

   return result

if dfs(di, 1):
   outp.write("NO")
else:
   outp.write("YES")