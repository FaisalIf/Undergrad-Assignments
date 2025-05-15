inp = open('input1.txt', 'r')
outp = open('output1.txt', 'w')

n, k = tuple(map(int, inp.readline().split()))

parent = [None]*(n+1)
child = [1]*(n+1)

def set_parent(x):
   parent[x] = x

def find(x):
   if parent[x] == x:
      return x
   return find(parent[x])

for i in range(n):
   set_parent(i)

for i in range(k):
   a, b = tuple(map(int, inp.readline().split()))
   u = find(a)
   v = find(b)

   if u != v:
      parent[u] = v
      child[v] += child[u]
      
   outp.write(f'{child[v]}\n')