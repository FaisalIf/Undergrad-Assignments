import heapq

inp = open('input3.txt', 'r')
outp = open('output3.txt', 'w')
v, e = tuple(map(int, inp.readline().split()))

adj = [[] for i in range(v+1)]
dist = [float('inf')]*(v+1)
par = [None]*(v+1)

for i in range(e):
   a, b, c = tuple(map(int, inp.readline().split()))
   adj[a].append((b, c))

def min_danger(src):

   dist[src] = 0
   pq = [(0, src)]

   while pq:
      d, u = heapq.heappop(pq)
      
      for v, w in adj[u]:
         if dist[v] > w:
            dist[v] = w
            par[v] = u
            heapq.heappush(pq, (dist[v], v))

min_danger(1)

max = -float('inf')
current = v

while current != 1:
   if current == None:
      max = 'Impossible'
      break
   if max < dist[current]:
      max = dist[current]
   current = par[current]

outp.write(f'{max}')