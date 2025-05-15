inp = open("input6.txt", "r")
outp = open("output6.txt", "w")

n, m = tuple(map(int, inp.readline().split(" ")))
grid = inp.read().split("\n")
visit = [[False for i in range(m)] for j in range(n)]

row = [0, -1, 0, 1]
col = [1, 0, -1, 0]

def valid(r, c):
   return 0<=r<n and 0<=c<m
def enqueue(q, v):
   q.append(v)
def dequeue(q):
   return q.pop(0)
def max(a, b):
   if a >= b:
      return a
   return b

def bfs_grid(r, c):

   count = 0
   if visit[r][c] == False and grid[r][c] != "#":
      visit[r][c] = True
      q = []
      enqueue(q, (r, c))

      while len(q) != 0:
         r, c = dequeue(q)

         if grid[r][c] == "D":
            count += 1

         for i in range(4):
            nr = r + row[i]
            nc = c + col[i]

            if valid(nr, nc) and not visit[nr][nc] and grid[nr][nc] != "#":
               visit[nr][nc] = True
               enqueue(q, (nr, nc))
               
   return count

max_count = 0
for i in range(n):
   for j in range(m):
      max_count = max(max_count, bfs_grid(i, j))

outp.write(str(max_count))