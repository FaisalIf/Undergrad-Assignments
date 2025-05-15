def dfs(g):
   for i in g.keys():
      if color[i] == "white" and i != 0:
         dfs_visit(g, i)

def dfs_visit(g, u):

   global cycle
   color[u] = 'gray'

   for v in g[u]:

      if color[v] == 'gray':
         cycle = True
         return
      
      if color[v] == 'white':
         dfs_visit(g, v)

   color[u] = 'black'
   stack.append(u)
   
inp = open('input1a.txt', 'r')
outp = open('output1a.txt', 'w')
v, e = tuple(map(int, inp.readline().split()))
di = {}

for i in range(v+1):
   di[i] = []
for i in range(e):
   a, b = tuple(map(int, inp.readline().split()))
   di[a].append(b)

color = ['white']*(v+1)
cycle = False
stack = []

dfs(di)

if cycle == False:
   for i in range(len(stack)):
      outp.write(f"{stack.pop()} ")
else:
   outp.write("IMPOSSIBLE")