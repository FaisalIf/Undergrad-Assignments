inp = open('input2.txt', 'r')
outp = open('output2.txt', 'w')
n, k = tuple(map(int, inp.readline().split()))

parent = [0]*(n+1)
road = [None]*(k)

def set_parent(x):
   parent[x] = x

def find(x):
   if parent[x] == x:
      return x
   return find(parent[x])

for i in range(n):
   set_parent(i)

for i in range(k):
   a, b, c = tuple(map(int, inp.readline().split()))
   road[i] = (c, a, b)

road.sort()

count = 0

for d, a, b in road:
   u = find(a)
   v = find(b)
   if u != v:
      parent[u] = v
      count += d

outp.write(f'{count}')