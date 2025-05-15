import heapq

inp = open('input1.txt', 'r')
outp = open('output1.txt', 'w')
v, e = tuple(map(int, inp.readline().split()))

adj = [[] for i in range(v+1)]
dist = [float('inf')]*(v+1)
par = [None]*(v+1)

for i in range(e):
   a, b, c = tuple(map(int, inp.readline().split()))
   adj[a].append((b, c))

src = int(inp.readline())

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

dijkstra(src)

for i in range(1, len(dist)):
   if dist[i] != float('inf'):
      outp.write(f"{dist[i]} ")
   else:
      outp.write(f"{-1} ")