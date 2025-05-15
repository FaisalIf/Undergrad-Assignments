inp = open("input2.txt", "r")
outp = open("output2.txt", "w")

v, e = tuple(map(int, inp.readline().split(" ")))
di = {}

for i in range(v+1):
   di[i] = []
for i in range(e):
   a, b = tuple(map(int, inp.readline().split(" ")))
   di[a].append((b))

def enqueue(q, v):
   q.append(v)
def dequeue(q):
   return q.pop(0)

def bfs(g, s):

   colour = [0]*(v+1)
   q = []
   colour[s] = 1
   enqueue(q, s)

   while len(q) != 0:
      outp.write(str(q[0])+" ")
      u = dequeue(q)
      
      for i in g[u]:
         if colour[i] == 0:
            colour[i] = 1
            enqueue(q, i)

bfs(di, 1)