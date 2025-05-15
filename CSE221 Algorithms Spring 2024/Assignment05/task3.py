def dfs(g):
   for i in g.keys():
      if color[i] == "white" and i != 0:
         dfs_visit(g, i)

def dfs_visit(g, u):

   color[u] = 'gray'
   for v in g[u]:

      if color[v] == 'white':
         dfs_visit(g, v)

   color[u] = 'black'
   stack.append(u)

def transpose_dfs(g, s):

   visited[s] = True
   for v in g[s]:

      if visited[v] == False:
         visited[v] = True
         transpose_dfs(g, v)

   temp.append(s)

inp = open('input3.txt', 'r')
outp = open('output3.txt', 'w')

v, e = tuple(map(int, inp.readline().split()))
di = {}
dit = {}

for i in range(v+1):
   di[i] = []
   dit[i] = []
for i in range(e):
   a, b = tuple(map(int, inp.readline().split()))
   di[a].append(b)
   dit[b].append(a)

color = ['white']*(v+1)
stack = []

dfs(di)

visited = [False]*(v+1)
connected = []

for i in range(len(stack)):
   temp = []
   top = stack.pop()

   if visited[top] == False:
      transpose_dfs(dit, top)
      
   temp.sort()
   connected.append(temp)

connected.sort()

for i in connected:
   if len(i) > 0:
      for j in i:
         outp.write(f"{j} ")
      outp.write("\n")