import heapq

def bfs(g):
   q = []
   for i in range(1, len(indeg)):
      if indeg[i] == 0:
         heapq.heappush(q, i)
         visited[i] = True

   while len(q) != 0:
      u = heapq.heappop(q)
      sorted.append(u)
      for v in g[u]:
         indeg[v] -= 1
         if indeg[v] == 0 and visited[v] == False:
            visited[v] = True
            heapq.heappush(q, v)

inp = open('input2.txt', 'r')
outp = open('output2.txt', 'w')
v, e = tuple(map(int, inp.readline().split()))
di = {}

indeg = [0]*(v+1)
visited = [False]*(v+1)

for i in range(v+1):
   di[i] = []
for i in range(e):
   a, b = tuple(map(int, inp.readline().split()))
   di[a].append(b)
   indeg[b] += 1

sorted = []
            
bfs(di)

cycle = False
for i in indeg:
   if i != 0:
      cycle = True
      break

if cycle == False:
   for i in sorted:
      outp.write(f'{i} ')
else:
   outp.write('IMPOSSIBLE')