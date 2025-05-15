inp = open("input3.txt", "r")
outp = open("output3.txt", "w")

v, e = tuple(map(int, inp.readline().split(" ")))
di = {}

for i in range(v+1):
   di[i] = []
for i in range(e):
   a, b = tuple(map(int, inp.readline().split(" ")))
   di[a].append((b))

colour = [0]*(v+1)

def dfs(g, s):
  
  colour[s] = 1
  outp.write(f"{s} ")

  for v in g[s]:
    if colour[v] == 0:
      dfs(g, v)

dfs(di, 1)