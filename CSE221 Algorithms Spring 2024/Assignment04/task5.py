inp = open("input5.txt", "r")
outp = open("output5.txt", "w")

v, e, n = tuple(map(int, inp.readline().split(" ")))
di = {}

for i in range(v+1):
   di[i] = []
for i in range(e):
   a, b = tuple(map(int, inp.readline().split(" ")))
   di[a].append(b)
   di[b].append(a)

def enqueue(q, v):
   q.append(v)
def dequeue(q):
   return q.pop(0)

def bfs(g, s):

   d = [0]*(v+1)
   p = [None]*(v+1)
   colour = [0]*(v+1)
   q = []
   colour[s] = 1
   enqueue(q, s)

   while len(q) != 0:
      u = dequeue(q)

      for i in g[u]:
         if colour[i] == 0:
            colour[i] = 1
            d[i] = d[u]+1
            p[i] = u
            enqueue(q, i)

   return d, p

d, p = bfs(di, 1)

if n != 1:
   path = [n]
   i = p[n]

   while i != 1:
      path.append(i)
      i = p[i]
   path.append(1)
   
else:
   path = [1]

outp.write(f"Time: {d[n]}\nShortest Path: ")
for i in range(len(path)-1, -1, -1):
   outp.write(f"{path[i]} ")