import heapq

inp = open('input2.txt', 'r')
outp = open('output2.txt', 'w')
v, e = tuple(map(int, inp.readline().split()))

adj = [[] for i in range(v+1)]
dist = [float('inf')]*(v+1)
par = [None]*(v+1)

for i in range(e):
   a, b, c = tuple(map(int, inp.readline().split()))
   adj[a].append((b, c))

src1, src2 = tuple(map(int, inp.readline().split()))

def dijkstra(src):

   dist[src] = 0
   pq = [(0, src)]

   while pq:
      d, u = heapq.heappop(pq)
      
      for v, w in adj[u]:
         if dist[v] > dist[u] + w:
            dist[v] = dist[u] + w
            par[v] = u
            heapq.heappush(pq, (dist[v], v))

def max(a, b):
   if a >= b:
      return a
   return b

dijkstra(src1)
dist1 = dist.copy()

dist = [float('inf')]*(v+1)
par = [None]*(v+1)

dijkstra(src2)
dist2 = dist.copy()

time = float('inf')
node = None

for i in range(1, len(dist)):
   if time > max(dist1[i], dist2[i]):
      time = max(dist1[i], dist2[i])
      node = i

if node != None:
   outp.write(f'Time {time}\nNode {node}')
else:
   outp.write('Impossible')